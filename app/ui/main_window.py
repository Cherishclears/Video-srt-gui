# coding:utf-8
import sys

from PySide6.QtCore import Qt, QUrl,Slot
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, InfoBar, InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF

from ..view.homeInterface import homeInterface
from ..view.downvideoInterface import downvideoInterface
from ..view.demucsInterface import demucsInterface
from ..view.modelInterface import modelInterface
from ..view.fasterwhisperInterface import FasterWhisperInterface
from ..view.transcription import transcriptionInterface

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        # 创建子接口
        self.homeInterface = homeInterface()
        self.downvideoInterface = downvideoInterface(self)
        self.demucsInterface = demucsInterface(self)
        self.modelInterface =modelInterface(self)
        self.whisperInterface = FasterWhisperInterface(self)
        self.transcriptionInterface = transcriptionInterface(self)
        # self.downvideoInterface = Widget('Download Video Interface', self)


        # 初始化导航栏
        self.initNavigation()
        # 初始化界面
        self.initWindow()
        # 连接信号
        self.connectSignals()

    def connectSignals(self):
        """连接信号"""
        # 连接首页界面发出的导航信号
        self.homeInterface.navigateToInterface.connect(self.navigateToInterface)

        self.modelInterface.modelLoaded.connect(self.onModelLoaded)

    def initNavigation(self):

        # 把创建的接口添加到导航栏
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")

        self.navigationInterface.addSeparator()  # 分割线

        self.addSubInterface(self.downvideoInterface, FIF.DOWN, "视频下载",NavigationItemPosition.SCROLL)
        self.addSubInterface(self.demucsInterface, FIF.MUSIC, "音频分离", NavigationItemPosition.SCROLL)
        self.addSubInterface(self.modelInterface, FIF.PAGE_RIGHT, "加载模型", NavigationItemPosition.SCROLL)
        self.addSubInterface(self.whisperInterface, FIF.SETTING, "参数设置", NavigationItemPosition.SCROLL)
        self.addSubInterface(self.transcriptionInterface, FIF.HEADPHONE, "转录", NavigationItemPosition.SCROLL)
        # 添加作者信息
        # self.navigationInterface.addWidget(
        #     routeKey='cherish',
        #     widget=NavigationAvatarWidget('cherish', 'resource/shoko.png'),
        #     onClick=self.showMessageBox,
        #     position=NavigationItemPosition.BOTTOM,
        # )


    def initWindow(self):
        self.resize(1200, 900) # 设置窗口大小
        self.setWindowIcon(QIcon('resources/images/1.jpg'))  # 添加应用图标
        self.setWindowTitle('未闻花落')    # 窗口主题

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        # 将窗口居中显示

    @Slot(str)
    def navigateToInterface(self, route):
        """处理导航信号"""
        # 根据路由导航到对应界面
        routeMap = {
            "download": self.downvideoInterface,
             "demucs": self.demucsInterface,
             "model": self.modelInterface,
             "whisper": self.whisperInterface,
             "transcription": self.transcriptionInterface,
            # "batch": self.batchInterface
        }

        # 如果找到匹配的路由，则切换到对应界面
        if route in routeMap:
            self.switchTo(routeMap[route])

    def onModelLoaded(self, model):
        """模型加载完成"""
        # 将模型传递给转录界面
        self.transcriptionInterface.setModel(model)

        # 获取Whisper参数设置并传递给转录界面
        whisper_params = self.fasterwhisperInterface.getParameters()
        self.transcriptionInterface.setWhisperParameters(whisper_params)

        # 切换到转录界面
        self.switchTo(self.transcriptionInterface)

        # 显示成功消息
        InfoBar.success(
            title="模型加载成功",
            content="已成功加载模型并应用参数设置",
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)     # label标签
        self.hBoxLayout = QHBoxLayout(self)           # 创建一个水平布局（QHBoxLayout），用于管理子控件的排列方式。

        setFont(self.label, 24)   # 设置字体
        self.label.setAlignment(Qt.AlignCenter)         # 设置标签的文本对齐方式为居中对齐。Qt.AlignCenter 是 Qt 中的一个枚举值，表示居中对齐。
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        # 将 self.label 添加到水平布局中。
        # 参数：
        # self.label：要添加的控件。
        # 1：控件的拉伸因子（stretch factor），表示标签在布局中占据的比例。
        # Qt.AlignCenter：控件在布局中的对齐方式为居中对齐。
        self.setObjectName(text.replace(' ', '-'))


