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


bl_info = {
    "name": "Companion1 Hologram Setup",
    "author": "S. 'Walter' Ji",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Companion1 Hologram Setup",
    'wiki_url': 'https://github.com/709924470/blender-c1-holoscreen-addon',
    "description": "在场景内新建一个空物体和相机, 并且自动旋转和渲染40角度的图像序列",
    "category": "Render",
}

import bpy
import math
import os
from bpy.types import (Panel, Operator)
from bpy.props import FloatProperty, StringProperty

class RENDER_OT_setup_camera(Operator):
    bl_idname = "render.setup_camera"
    bl_label = "新建相机"
    bl_description = "新建一个空物体(旋转中心点)和一个相机"
    
    def execute(self, context):
        if bpy.data.objects.get("相机旋转中心点") or bpy.data.objects.get("C1视角"):
            self.report({'ERROR'}, "检测到已创建相机, 请勿重新创建!")
            return {'CANCELLED'}
        
        # Create empty as pivot
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        empty = bpy.context.active_object
        empty.name = "相机旋转中心点"
        
        # Create camera for rendering
        bpy.ops.object.camera_add(location=(0, -5, 0))
        camera = bpy.context.active_object
        camera.name = "C1视角"
        
        # Point camera to the pivot
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = empty
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
        
        # Parent camera to empty
        camera.parent = empty
        
        # Make this camera active
        context.scene.camera = camera

        # Change render resolution to 450x800
        render = context.scene.render
        render.resolution_x = 450
        render.resolution_y = 800
        render.resolution_percentage = 100
        
        return {'FINISHED'}

class RENDER_OT_render_angles(Operator):
    bl_idname = "render.render_angles"
    bl_label = "渲染视差图形序列"
    bl_description = "渲染视差图像序列(注意先保存文件到单独的文件夹)"
    
    output_path: StringProperty(
        name="Output Path",
        default="//renders/",
        description="图片存储路径",
        subtype='DIR_PATH'
    )
    
    def execute(self, context):
        empty = bpy.data.objects.get("相机旋转中心点")
        if not empty:
            self.report({'ERROR'}, "未找到相机! 请先点击新建相机!")
            return {'CANCELLED'}
        
        # Create output directory if it doesn't exist
        output_path = bpy.path.abspath(self.output_path)
        os.makedirs(output_path, exist_ok=True)
        
        # Store original rotation
        original_rotation = empty.rotation_euler.copy()
        
        # Render loop
        for i in range(40):
            empty.rotation_euler.z = original_rotation.z + math.radians(i - 20)
            
            # Update scene
            bpy.context.view_layer.update()
            
            # Render
            bpy.context.scene.render.filepath = os.path.join(output_path, f"render_{i:03d}.png")
            bpy.ops.render.render(write_still=True)
            
        # Restore original rotation
        empty.rotation_euler = original_rotation
        
        self.report({'INFO'}, f"渲染成功, 已将图片保存至 {output_path}")
        return {'FINISHED'}

class VIEW3D_PT_render_angles(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Companion1 Hologram Setup"
    bl_label = "Companion1 Hologram Setup"
    
    def draw(self, context):
        layout = self.layout
        
        # Info
        box = layout.box()
        box.label(text="使用指南:", icon='INFO')
        box.label(text="1. 点击 `新建相机`")
        box.label(text="2. 调整相机位置")
        box.label(text="3. 调整渲染设置,")
        box.label(text="        注意不要变更分辨率")
        box.label(text="        记得先保存当前场景")
        box.label(text="4. 点击 `渲染视差图形序列`")
        box.label(text="5. 使用其他工具将图像序列转换为")
        box.label(text="        单张的图片矩阵, 并导出为视频")
        box.label(text="-"*30)
        box.label(text="入屏效果: 将中心点放在画面主体前方")
        box.label(text="出屏效果: 将中心点放在画面主体后方")
        
        layout.separator()
        
        layout.operator("render.setup_camera", icon='CAMERA_DATA')
        
        layout.separator()
        
        op = layout.operator("render.render_angles", icon='RENDER_STILL')
        op.output_path = "//renders/"

def register():
    bpy.utils.register_class(RENDER_OT_setup_camera)
    bpy.utils.register_class(RENDER_OT_render_angles)
    bpy.utils.register_class(VIEW3D_PT_render_angles)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_render_angles)
    bpy.utils.unregister_class(RENDER_OT_render_angles)
    bpy.utils.unregister_class(RENDER_OT_setup_camera)

if __name__ == "__main__":
    register()