# SPDX-License-Identifier: GPL-3.0-or-later

# Companion1 Blender exporter Addon
# Copyright (C) 2024 S. Walter Ji
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cv2
import numpy as np
import glob
import subprocess
from pathlib import Path
from argparse import ArgumentParser

def create_matrix_frame(image_paths, rows=5, cols=8):
    # Read first image to get dimensions
    first_img = cv2.imread(image_paths[0])
    h, w = first_img.shape[:2]
    
    # Create blank canvas
    matrix = np.zeros((h * rows, w * cols, 3), dtype=np.uint8)
    
    # Place images in matrix
    for idx, img_path in enumerate(image_paths):
        if idx >= rows * cols:  # Stop after 40 images
            break
            
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        # Calculate position
        row = idx // cols
        col = idx % cols
        
        # Place image in matrix
        matrix[row*h:(row+1)*h, col*w:(col+1)*w] = img
    
    return matrix

def main(img_path, out_path, save_matrix):
    # Get all PNG files sorted by name
    full_path = Path(img_path)
    image_files = sorted(full_path.absolute().glob( "*.png"))
    
    if len(image_files) < 40:
        print(f"Error: Found only {len(image_files)} PNG files. Need 40 files.")
        return
    
    # Create matrix frame
    frame = create_matrix_frame(image_files[:40])
    
    # Save frame as temporary PNG
    output_path = Path(out_path).absolute()
    temp_frame = output_path / 'temp_matrix.png'
    cv2.imwrite(temp_frame, frame)
    
    # Use ffmpeg to create video
    output_file = output_path / 'output_matrix.mp4'
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-loop', '1',  # Loop the input
        '-i', temp_frame,  # Input file
        '-c:v', 'libx265',  # Use H.265 codec
        '-crf', '23',  # Constant Rate Factor (adjust for quality vs size, 0-51, lower is better quality)
        '-preset', 'medium',  # Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
        '-tag:v', 'hvc1',  # Add tag for better compatibility with Apple devices
        '-t', '1',  # Duration in seconds
        '-pix_fmt', 'yuv420p',  # Pixel format
        '-vf', 'fps=30',  # Frame rate
        str(output_file.absolute())
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Video saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg: {e}")
    finally:
        # Clean up temporary file
        import os
        if os.path.exists(temp_frame) and not save_matrix:
            os.remove(temp_frame)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="这个脚本用来将C1-blender-addon渲染出的40张图像序列转换为3D Player所需要的视频格式",
        )
    parser.add_argument("image_path", help="包含40张图片序列的文件夹路径, 默认当前文件夹", default=".")
    parser.add_argument("out_path", help="输出文件夹路径, 默认当前文件夹, 或输入文件夹路径", nargs="?")
    parser.add_argument("--save", help="不删除生成视频用到的单张矩阵图片", action="store_true")
    args = parser.parse_args()
    main(args.image_path, args.out_path or args.image_path, args.save)