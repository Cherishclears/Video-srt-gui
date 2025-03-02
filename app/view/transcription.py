from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from qfluentwidgets import InfoBar, InfoBarPosition, ToolButton, FluentIcon as FIF

import os
import torch
import time
from pathlib import Path
from datetime import timedelta

from app.ui.Ui_transcription import Ui_transcription


class TranscriptionWorker(QThread):
    update_progress_signal = Signal(str, str)  # 文件路径, 状态
    transcription_finished_signal = Signal(str, bool, str)  # 文件路径, 成功/失败, 消息

    def __init__(self, file_path, model, output_path, params):
        super().__init__()
        self.file_path = file_path
        self.model = model
        self.output_path = output_path
        self.params = params
        self.is_running = False

    def run(self):
        self.is_running = True

        try:
            # 更新状态为处理中
            self.update_progress_signal.emit(self.file_path, "处理中...")

            # 确保输出目录存在
            os.makedirs(self.output_path, exist_ok=True)

            # 获取文件名
            file_name = os.path.basename(self.file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]

            # 转写音频
            segments, info = self.model.transcribe(
                self.file_path,
                **self.params
            )

            # 保存为SRT字幕文件
            srt_file_path = os.path.join(self.output_path, file_name_without_ext + ".srt")
            self.save_to_srt(segments, srt_file_path)

            # 保存为TXT文本文件
            txt_file_path = os.path.join(self.output_path, file_name_without_ext + ".txt")
            self.save_to_txt(segments, txt_file_path)

            # 发送完成信号
            self.transcription_finished_signal.emit(
                self.file_path,
                True,
                f"转录完成: {file_name}\n语言: {info.language}\n可信度: {info.language_probability:.2f}"
            )

        except Exception as e:
            # 发送错误信号
            self.transcription_finished_signal.emit(self.file_path, False, f"错误: {str(e)}")

        self.is_running = False

    def stop(self):
        self.is_running = False

    def save_to_srt(self, segments, output_file):
        """保存为SRT字幕格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, start=1):
                # 计算开始和结束时间
                start_time = self.format_timestamp(segment.start)
                end_time = self.format_timestamp(segment.end)

                # 写入SRT格式
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment.text.strip()}\n\n")

    def save_to_txt(self, segments, output_file):
        """保存为纯文本格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for segment in segments:
                f.write(f"{segment.text.strip()}\n")

    def format_timestamp(self, seconds):
        """将秒数转换为SRT时间戳格式 (HH:MM:SS,mmm)"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


class transcriptionInterface(QWidget, Ui_transcription):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 初始化变量
        self.model = None
        self.workers = {}  # 存储每个文件对应的工作线程

        # 初始化输出路径
        self.output_path = os.path.join(os.getcwd(), "output", "transcription")
        self.outputGroupWidget.lineEdit.setText(self.output_path)

        # 连接信号
        self.connectSignals()

    def connectSignals(self):
        """连接所有信号"""
        self.fileListView.fileListChanged.connect(self.updateFileList)
        self.outputGroupWidget.toolButton.clicked.connect(self.selectOutputPath)
        self.startButton.clicked.connect(self.startTranscription)

    def setModel(self, model):
        """设置转录模型"""
        self.model = model
        if self.model:
            self.modelStatusLabel.setText("模型已加载!")
            self.modelStatusLabel.setStyleSheet(
                "background-color: rgba(0, 255, 0, 0.3); padding: 10px; border-radius: 5px;")
        else:
            self.modelStatusLabel.setText("模型未加载!")
            self.modelStatusLabel.setStyleSheet(
                "background-color: rgba(255, 0, 0, 0.3); padding: 10px; border-radius: 5px;")

    def selectOutputPath(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择保存路径",
            self.output_path
        )
        if dir_path:
            self.output_path = dir_path
            self.outputGroupWidget.lineEdit.setText(dir_path)

    def updateFileList(self, files):
        """更新文件列表"""
        # 清空表格
        self.fileTableWidget.setRowCount(0)

        # 添加文件到表格
        for i, file_path in enumerate(files):
            file_name = os.path.basename(file_path)

            # 创建新行
            self.fileTableWidget.insertRow(i)

            # 设置文件名
            self.fileTableWidget.setItem(i, 0, QTableWidgetItem(file_name))

            # 设置状态
            self.fileTableWidget.setItem(i, 1, QTableWidgetItem("等待中"))

            # 创建操作按钮
            buttonWidget = QWidget()
            buttonLayout = QHBoxLayout(buttonWidget)
            buttonLayout.setContentsMargins(0, 0, 0, 0)
            buttonLayout.setSpacing(4)

            # 创建转录按钮
            transcribeButton = ToolButton()
            transcribeButton.setIcon(FIF.PLAY)
            transcribeButton.setToolTip("开始转录")
            transcribeButton.clicked.connect(lambda checked=False, fp=file_path: self.startSingleTranscription(fp))

            # 创建取消按钮
            cancelButton = ToolButton()
            cancelButton.setIcon(FIF.CANCEL)
            cancelButton.setToolTip("取消转录")
            cancelButton.clicked.connect(lambda checked=False, fp=file_path: self.cancelTranscription(fp))

            # 添加按钮到布局
            buttonLayout.addWidget(transcribeButton)
            buttonLayout.addWidget(cancelButton)
            buttonLayout.addStretch()

            # 设置操作列
            self.fileTableWidget.setCellWidget(i, 2, buttonWidget)

    def startTranscription(self):
        """开始所有文件的转录"""
        # 检查模型是否已加载
        if not self.model:
            InfoBar.error(
                title="错误",
                content="模型未加载，请先在'加载模型'界面加载模型",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 获取文件列表
        files = self.fileListView.getFileList()
        if not files:
            InfoBar.error(
                title="错误",
                content="请先添加需要转录的文件",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 获取输出路径
        output_path = self.outputGroupWidget.lineEdit.text()
        if not output_path:
            InfoBar.error(
                title="错误",
                content="请设置输出目录",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 获取当前已加载模型的参数
        params = {
            "language": None,  # 自动检测语言
            "task": "transcribe",  # 转录任务
            "beam_size": 5,  # 默认波束大小
            "word_timestamps": True,  # 生成单词级时间戳
        }

        # 遍历文件列表，开始转录
        for file_path in files:
            self.startSingleTranscription(file_path, params)

    def startSingleTranscription(self, file_path, params=None):
        """开始单个文件的转录"""
        # 检查模型是否已加载
        if not self.model:
            InfoBar.error(
                title="错误",
                content="模型未加载，请先在'加载模型'界面加载模型",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 检查文件是否存在
        if not os.path.exists(file_path):
            InfoBar.error(
                title="错误",
                content=f"文件不存在: {file_path}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 获取输出路径
        output_path = self.outputGroupWidget.lineEdit.text()
        if not output_path:
            InfoBar.error(
                title="错误",
                content="请设置输出目录",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 如果没有提供参数，使用默认参数
        if params is None:
            params = {
                "language": None,  # 自动检测语言
                "task": "transcribe",  # 转录任务
                "beam_size": 5,  # 默认波束大小
                "word_timestamps": True,  # 生成单词级时间戳
            }

        # 检查该文件是否已经在处理中
        if file_path in self.workers and self.workers[file_path].is_running:
            InfoBar.warning(
                title="警告",
                content=f"文件正在处理中: {os.path.basename(file_path)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 更新文件状态
        self.updateFileStatus(file_path, "准备中...")

        # 创建工作线程
        worker = TranscriptionWorker(file_path, self.model, output_path, params)
        self.workers[file_path] = worker

        # 连接信号
        worker.update_progress_signal.connect(self.updateFileStatus)
        worker.transcription_finished_signal.connect(self.onTranscriptionFinished)

        # 开始转录
        worker.start()

    def cancelTranscription(self, file_path):
        """取消转录"""
        if file_path in self.workers and self.workers[file_path].is_running:
            self.workers[file_path].stop()
            self.workers[file_path].wait()
            self.updateFileStatus(file_path, "已取消")

            InfoBar.info(
                title="已取消",
                content=f"已取消文件转录: {os.path.basename(file_path)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
        else:
            InfoBar.info(
                title="提示",
                content=f"文件未在处理中: {os.path.basename(file_path)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )

    def updateFileStatus(self, file_path, status):
        """更新文件状态"""
        file_name = os.path.basename(file_path)

        # 查找对应的行
        for i in range(self.fileTableWidget.rowCount()):
            if self.fileTableWidget.item(i, 0).text() == file_name:
                # 更新状态列
                self.fileTableWidget.setItem(i, 1, QTableWidgetItem(status))
                break

    def onTranscriptionFinished(self, file_path, success, message):
        """转录完成处理"""
        file_name = os.path.basename(file_path)

        if success:
            self.updateFileStatus(file_path, "完成")
            InfoBar.success(
                title="转录完成",
                content=message,
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000
            )
        else:
            self.updateFileStatus(file_path, "失败")
            InfoBar.error(
                title="转录失败",
                content=message,
                parent=self,
                position=InfoBarPosition.TOP,
                duration=5000
            )