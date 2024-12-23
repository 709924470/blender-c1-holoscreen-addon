# 自由象限 Companion1 Blender 插件

⚠请注意：这是非官方插件，请在使用时遵守 GNU GPL v3.0 协议。
如果在使用中碰到问题，请在 Issue 中提交工单。

---

> 注意：截至 2024.12.23 日，C1 所需要的 3DPlayer 软件需要向官方申请内测获取。

本仓库包含：

- docs/ : 包含展示用文件
  - img_seq/ : 渲染出的图片序列
  - default_cube.blend : Blender 示例文件
  - output_matrix.mp4 : 可以直接在 3Dplayer 中使用的视频文件
  - temp_matrix.png: 使用图片序列生成的中间文件，调试&展示用
- `__init__.py` : Blender 插件脚本
- `converter.py` : 转换脚本

---

## 使用说明：

### 安装 Blender 插件

0. [点击此处下载本插件的压缩包](https://github.com/709924470/blender-c1-holoscreen-addon/archive/refs/heads/master.zip)
1. 打开 Blender, 在 Blender 中选择 `编辑 > 首选项 > 插件 > 从硬盘安装`
2. 在弹出的文件选择框中找到下载到的位置安装
3. 在 Blender 的插件管理界面，找到 `c1_exporter`并启用

### 使用插件

1. 在 Blender 的 3D 视窗中按下 N 来打开/关闭右侧面板
2. 打开右侧面板
3. 向下滚动找到 `Companion1 Hologram Setup` 并点击
4. 按照面板提示内容进行操作即可

![screen_shot](https://github.com/user-attachments/assets/18bc051e-c324-47a6-9026-b033f1624d39)

### 使用转换脚本 `converter.py`

> 注意：你可以将这个脚本移动到任意位置

0. 你需要先安装
   - Python 3.10 以上版本
   - 安装 Python 后通过命令行，输入 `pip install opencv-python`来安装 opencv
   - ffmpeg, 将软件放在与此脚本同一目录下或环境变量 `PATH`内任意文件夹下
1. 打开命令行，使用 `cd`指令导航到存放此脚本的目录
2. 使用 `python converter.py X:/完整的/图片/路径/ Y:/完整的/输出/路径(可省略)`来运行脚本，你可以通过在结尾添加 ` -h`来查看使用方法

如果不出意外你将会得到一个包含渲染出来的视频文件，此文件可以直接在 3d player 中使用。

<summary>
<detail>视差网格样例<detail/>

网格图片:

![temp_matrix](https://github.com/user-attachments/assets/a325ad19-6c9c-4730-a5a5-118ad9813194)

网格视频:

https://github.com/user-attachments/assets/1c0ce87d-50ff-4700-9ce8-3009c96ea9e3

<summary/>
