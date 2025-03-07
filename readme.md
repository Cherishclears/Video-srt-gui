# 未闻花落 - 音视频处理工具

![1](./resources/images/1.jpg)

## 项目简介

这是一款功能全面的音视频处理工具，基于PySide6开发的桌面应用程序，集成了视频下载、音频分离、语音转录等多种功能于一体。应用采用了PySide6-Fluent-Widgets作为UI框架，提供了现代化、美观的用户界面和良好的用户体验。

## 功能特点

### 视频下载

- 支持从多个平台（如YouTube、Bilibili等）下载视频
- 支持选择不同的视频质量和格式
- 支持使用Cookies文件下载需要登录的网站内容
- 实时显示下载进度

### 音频分离

- 使用先进的Demucs模型进行音频分离
- 支持分离人声、背景声、贝斯、鼓点等音轨
- 可自定义分段长度和重叠度以优化分离效果
- 批量处理多个音频文件

### 语音转录

- 基于faster-whisper模型实现高质量语音转录
- 支持多语言自动识别和转录
- 支持生成SRT字幕和纯文本格式转录结果
- 可设置丰富的转录参数，满足不同场景需求

### 其他功能

- 支持拖放文件到应用中进行处理
- 提供详细的操作日志和处理状态
- 统一的输出目录管理

## 系统要求

- **操作系统**：Windows、macOS 或 Linux
- **Python版本**：3.8或更高版本
- **GPU支持**：推荐使用支持CUDA的NVIDIA显卡以加速音频分离和语音转录功能
- **磁盘空间**：至少10GB可用空间（用于应用程序、模型和处理的文件）

## 安装指南

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

安装的主要依赖包括：

- pyside6
- Pyside6-Fluent-Widgets
- torch (CUDA版本)
- torchaudio (CUDA版本)
- faster-whisper
- yt-dlp
- ffmpeg-python
- scipy
- soundfile

### 2. 启动应用

```bash
python main.py
```

## 使用指南

### 视频下载

1. 在导航栏选择"视频下载"
2. 输入需要下载的视频URL
3. 可选择提供Cookies文件（对于需要登录的网站）
4. 点击"查询视频信息"获取可用的视频格式
5. 选择合适的视频质量和输出路径
6. 点击"开始下载"

### 音频分离

1. 在导航栏选择"音频分离"
2. 添加需要处理的音频文件（支持拖放）
3. 设置分离参数（如采样重叠度、分段长度）
4. 选择输出音轨类型（全部、仅人声、仅背景声等）
5. 设置输出目录
6. 点击"提取"开始处理

### 语音转录

1. 在导航栏依次选择"加载模型"和"参数设置"配置转录环境
2. 加载语音模型（支持本地模型）
3. 设置转录参数（如语言、格式等）
4. 在"转录"界面添加需要转录的音频或视频文件
5. 设置输出目录
6. 点击"开始"进行转录
7. 完成后可查看生成的SRT字幕文件和文本文件

## 技术架构

- **UI框架**：PySide6 + Pyside6-Fluent-Widgets
- **音频分离**：Demucs (torchaudio.pipelines.HDEMUCS_HIGH_MUSDB_PLUS)
- **语音转录**：faster-whisper
- **视频下载**：yt-dlp
- **音频处理**：torchaudio、scipy、soundfile

## 注意事项

- 音频分离功能非常消耗系统资源，建议使用配置较高的计算机
- 首次运行时，程序会自动下载相关模型文件，请确保网络连接正常
- 为获得最佳性能，建议使用支持CUDA的NVIDIA显卡

## 常见问题

### Q: 模型下载失败怎么办？

A: 请检查网络连接，或手动将模型文件放置在相应目录下。

### Q: 程序运行时内存占用过高？

A: 音频分离和语音转录功能需要较大内存，可以尝试减小处理的音频段落长度来降低内存使用。

### Q: 支持哪些视频网站下载？

A: 支持YouTube、Bilibili等大多数主流视频网站，详细列表可点击应用中的"支持的网站列表"链接查看。

## 致谢

- PySide6-Fluent-Widgets：提供了现代化的UI组件
- faster-whisper：提供了高效的语音转录功能
- Demucs：提供了优秀的音频分离算法
- yt-dlp：提供了强大的视频下载功能