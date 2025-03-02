import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal
from app.ui.Ui_downvideo import Ui_downvideo
from qfluentwidgets import InfoBar, InfoBarPosition
import yt_dlp


class DownloadThread(QThread):
    progress_signal = Signal(float, str)
    finished_signal = Signal(bool, str)

    def __init__(self, url, format_id, output_path, cookies_path=None):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.output_path = output_path
        self.cookies_path = cookies_path

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            p = p.replace('%', '')
            try:
                percentage = float(p)
                self.progress_signal.emit(percentage, d.get('_eta_str', ''))
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_signal.emit(100, "处理中...")

    def run(self):
        try:
            ydl_opts = {
                'format': self.format_id,
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
            }

            if self.cookies_path and os.path.exists(self.cookies_path):
                ydl_opts['cookiefile'] = self.cookies_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.finished_signal.emit(True, "下载完成！")
        except Exception as e:
            self.finished_signal.emit(False, f"下载失败: {str(e)}")


class InfoThread(QThread):
    info_signal = Signal(dict)
    error_signal = Signal(str)

    def __init__(self, url, cookies_path=None):
        super().__init__()
        self.url = url
        self.cookies_path = cookies_path

    def run(self):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }

            if self.cookies_path and os.path.exists(self.cookies_path):
                ydl_opts['cookiefile'] = self.cookies_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.info_signal.emit(info)
        except Exception as e:
            self.error_signal.emit(f"获取视频信息失败: {str(e)}")


class downvideoInterface(QWidget, Ui_downvideo):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 初始化变量
        self.output_path = os.path.join(os.getcwd(), "output")
        self.outputPathLabel.setText(self.output_path)
        os.makedirs(self.output_path, exist_ok=True)

        self.cookies_path = ""
        self.video_info = None
        self.formats = []

        # 连接信号
        self.connectSignals()

    def connectSignals(self):
        """连接所有按钮的信号"""
        self.cookiesButton.clicked.connect(self.select_cookies_file)
        self.outputButton.clicked.connect(self.select_output_path)
        self.queryButton.clicked.connect(self.query_video_info)
        self.downloadButton.clicked.connect(self.start_download)

    def select_cookies_file(self):
        """选择Cookies文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Cookies文件", "", "文本文件 (*.txt);;JSON文件 (*.json);;所有文件 (*.*)"
        )
        if file_path:
            self.cookies_path = file_path
            self.cookiesPathLabel.setText(file_path)

    def select_output_path(self):
        """选择输出路径"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择保存路径", self.output_path
        )
        if dir_path:
            self.output_path = dir_path
            self.outputPathLabel.setText(dir_path)

    def query_video_info(self):
        """查询视频信息"""
        url = self.urlInput.text().strip()
        if not url:
            self.show_info_bar("错误", "请输入视频URL", InfoBarPosition.TOP)
            return

        self.statusLabel.setText("正在获取视频信息...")
        self.formatCombo.clear()
        self.downloadButton.setEnabled(False)

        self.info_thread = InfoThread(url, self.cookies_path)
        self.info_thread.info_signal.connect(self.update_video_info)
        self.info_thread.error_signal.connect(self.show_error)
        self.info_thread.start()

    def update_video_info(self, info):
        """更新视频信息"""
        self.video_info = info
        self.videoTitleLabel.setText(f"视频标题: {info.get('title', '未知')}")

        self.formats = []
        # 获取可用的视频格式
        if 'formats' in info:
            for f in info['formats']:
                if f.get('vcodec', 'none') != 'none':  # 确保有视频流
                    format_id = f.get('format_id', '')
                    format_note = f.get('format_note', '')
                    resolution = f.get('resolution', '')
                    ext = f.get('ext', '')

                    # 创建格式描述
                    desc = f"{resolution} - {format_note} ({ext})"
                    if desc and format_id:
                        self.formats.append((format_id, desc))

        # 添加最佳质量选项
        self.formats.insert(0, ('best', '最佳质量 (自动选择)'))

        # 更新下拉框
        for format_id, desc in self.formats:
            self.formatCombo.addItem(desc, format_id)

        self.downloadButton.setEnabled(True)
        self.statusLabel.setText("视频信息获取成功，请选择画质并开始下载")

    def show_error(self, error_msg):
        """显示错误信息"""
        self.show_info_bar("错误", error_msg, InfoBarPosition.TOP, duration=5000)
        self.statusLabel.setText("发生错误")

    def start_download(self):
        """开始下载视频"""
        if not self.video_info:
            self.show_info_bar("错误", "请先获取视频信息", InfoBarPosition.TOP)
            return

        format_id = self.formatCombo.currentData()
        if not format_id:
            self.show_info_bar("错误", "请选择视频画质", InfoBarPosition.TOP)
            return

        self.progressBar.setValue(0)
        self.statusLabel.setText("准备下载...")
        self.downloadButton.setEnabled(False)

        self.download_thread = DownloadThread(
            self.urlInput.text().strip(),
            format_id,
            self.output_path,
            self.cookies_path
        )
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, percentage, eta):
        """更新下载进度"""
        self.progressBar.setValue(int(percentage))
        if eta:
            self.statusLabel.setText(f"下载中... 剩余时间: {eta}")
        else:
            self.statusLabel.setText("下载中...")

    def download_finished(self, success, message):
        """下载完成处理"""
        self.statusLabel.setText(message)
        self.downloadButton.setEnabled(True)

        if success:
            self.show_info_bar("成功", f"视频已下载到: {self.output_path}", InfoBarPosition.TOP,
                               duration=5000, type="success")
        else:
            self.show_info_bar("错误", message, InfoBarPosition.TOP, duration=5000)

    def show_info_bar(self, title, content, position, duration=3000, type="error"):
        """显示通知信息栏"""
        if type == "error":
            InfoBar.error(
                title=title,
                content=content,
                parent=self,
                position=position,
                duration=duration
            )
        elif type == "success":
            InfoBar.success(
                title=title,
                content=content,
                parent=self,
                position=position,
                duration=duration
            )
        else:
            InfoBar.info(
                title=title,
                content=content,
                parent=self,
                position=position,
                duration=duration
            )