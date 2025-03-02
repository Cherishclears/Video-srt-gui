from PySide6.QtCore import QSize, Qt, QMetaObject
from PySide6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QSizePolicy,
                               QFrame, QLabel, QLayout)
from PySide6.QtGui import QColor, QFont
from qfluentwidgets import (CardWidget, PrimaryPushButton, FluentIcon as FIF,
                            StrongBodyLabel, BodyLabel, ScrollArea, FlowLayout)


class Ui_home(object):
    def setupUi(self, homeInterface):
        if not homeInterface.objectName():
            homeInterface.setObjectName(u"homeInterface")

        # 设置主界面的垂直布局
        self.verticalLayout = QVBoxLayout(homeInterface)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName(u"verticalLayout")

        # 创建滚动区域
        self.scrollArea = ScrollArea(homeInterface)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条

        # 创建滚动区域内的容器部件
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setObjectName(u"scrollAreaContents")

        # 使用FlowLayout，自动适应窗口大小布局卡片
        self.flowLayout = FlowLayout(self.scrollAreaContents)
        self.flowLayout.setObjectName(u"flowLayout")
        self.flowLayout.setContentsMargins(10, 10, 10, 10)
        self.flowLayout.setHorizontalSpacing(20)
        self.flowLayout.setVerticalSpacing(20)

        # 设置滚动区域的窗口部件
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # 初始化卡片列表，方便后续管理
        self.cards = []
        self.cardButtons = []

        # 默认创建6个演示卡片
        self.createDemoCards()

        # 自定义按钮样式为粉色
        self.setPinkButtonStyle()

        QMetaObject.connectSlotsByName(homeInterface)

    def createDemoCards(self):
        """创建一些演示用的卡片"""
        demoTitles = ["视频下载","音频分离","加载模型","参数设置","转录"]
        # , "音频提取", "字幕生成", "视频剪辑", "格式转换", "批量处理"

        # 创建卡片并添加到布局中
        for title in demoTitles:
            # 创建卡片
            card = self.createCard(title)

            # 将卡片添加到流式布局中
            self.flowLayout.addWidget(card)

            # 存储卡片和按钮的引用，以便后续访问
            self.cards.append(card)

    def createCard(self, title):
        """创建一个卡片部件"""
        # 创建一个卡片部件
        card = CardWidget()
        card.setObjectName(f"card_{title}")

        # 设置卡片的尺寸策略和最小大小
        card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        card.setMinimumSize(400, 800)  # 设置最小大小，确保卡片高度足够
        card.setMaximumSize(800, 1000)  # 设置最大大小，防止卡片过大

        # 创建卡片内的垂直布局
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(16, 20, 16, 20)
        cardLayout.setSpacing(10)

        # 创建标题标签
        titleLabel = QLabel(title)
        titleLabel.setObjectName(f"label_{title}")
        titleLabel.setAlignment(Qt.AlignCenter)

        # 设置字体加大加黑
        font = QFont()
        font.setPointSize(20)  # 加大字体
        font.setBold(True)  # 加粗
        font.setWeight(QFont.Weight.Black)  # 更黑的权重
        titleLabel.setFont(font)

        # 创建"进入"按钮 - 粉色样式将在setPinkButtonStyle中设置
        enterButton = PrimaryPushButton("进入")
        enterButton.setObjectName(f"button_{title}")
        enterButton.setFixedSize(60, 30)  # 设置按钮大小

        # 将小部件添加到布局中
        cardLayout.addWidget(titleLabel, 0, Qt.AlignCenter)
        cardLayout.addStretch(1)  # 添加弹性空间
        cardLayout.addWidget(enterButton, 0, Qt.AlignCenter)
        cardLayout.addStretch(0)  # 底部添加少量空间

        # 保存按钮引用
        self.cardButtons.append(enterButton)

        return card

    def setPinkButtonStyle(self):
        """设置按钮为粉色样式"""
        # 粉色按钮样式表
        pinkButtonStyle = """
            PrimaryPushButton {
                background-color: #FF80AB;  /* 粉色背景 */
                border: 1px solid #FF80AB;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }

            PrimaryPushButton:hover {
                background-color: #FF4081;  /* 鼠标悬停时更深的粉色 */
                border-color: #FF4081;
            }

            PrimaryPushButton:pressed {
                background-color: #F50057;  /* 按下时更深的粉色 */
                border-color: #F50057;
            }
        """

        # 应用样式到所有按钮
        for button in self.cardButtons:
            button.setStyleSheet(pinkButtonStyle)