from PySide6.QtCore import QMetaObject, Qt, QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QSizePolicy, QFrame, QTableWidget, QTableWidgetItem,
                               QHeaderView, QAbstractItemView)
from PySide6.QtGui import QIcon
from qfluentwidgets import (CardWidget, PrimaryPushButton, BodyLabel, TitleLabel,
                            IconWidget, FluentIcon as FIF, TransparentPushButton,
                            ToolButton, ScrollArea)
from ..view.fileNameListViewInterface import FileNameListView
from ..view.outputLabelLineEditButtonWidget import OutputGroupWidget


class Ui_transcription(object):
    def setupUi(self, transcriptionInterface):
        if not transcriptionInterface.objectName():
            transcriptionInterface.setObjectName(u"transcriptionInterface")

        # 主布局
        self.verticalLayout = QVBoxLayout(transcriptionInterface)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(36, 10, 36, 10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setAlignment(Qt.AlignTop)

        # 标题部分
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setSpacing(16)

        self.titleLabel = TitleLabel(u"Transcription")
        self.subtitleLabel = BodyLabel(u"选择文件、字幕文件保存目录、转写文件")

        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.addStretch(1)

        self.verticalLayout.addLayout(self.titleLayout)
        self.verticalLayout.addWidget(self.subtitleLabel)

        # 模型状态提示
        self.modelStatusLabel = QLabel(u"模型未加载!")
        self.modelStatusLabel.setObjectName(u"modelStatusLabel")
        self.modelStatusLabel.setStyleSheet(
            "background-color: rgba(255, 0, 0, 0.3); padding: 10px; border-radius: 5px;")
        self.modelStatusLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.modelStatusLabel)

        # 文件列表视图
        self.fileListView = FileNameListView(transcriptionInterface)
        self.verticalLayout.addWidget(self.fileListView)

        # 输出设置
        self.outputGroupWidget = OutputGroupWidget(transcriptionInterface)
        self.verticalLayout.addWidget(self.outputGroupWidget)

        # 音视频文件列表显示
        self.tableCardWidget = CardWidget(transcriptionInterface)
        self.tableCardLayout = QVBoxLayout(self.tableCardWidget)
        self.tableCardLayout.setContentsMargins(20, 16, 20, 16)
        self.tableCardLayout.setSpacing(10)

        self.tableLabel = TitleLabel(u"音视频文件列表")
        self.tableCardLayout.addWidget(self.tableLabel)

        # 创建表格
        self.fileTableWidget = QTableWidget()
        self.fileTableWidget.setObjectName(u"fileTableWidget")
        self.fileTableWidget.setColumnCount(3)
        self.fileTableWidget.setHorizontalHeaderLabels([u"文件名", u"状态", u"操作"])
        self.fileTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.fileTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.fileTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.fileTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableCardLayout.addWidget(self.fileTableWidget)
        self.verticalLayout.addWidget(self.tableCardWidget)

        # 启动按钮
        self.startButtonLayout = QHBoxLayout()
        self.startButtonLayout.setContentsMargins(0, 10, 0, 10)

        self.startButton = PrimaryPushButton(u"开始")
        self.startButton.setIcon(FIF.PLAY)
        self.startButton.setFixedHeight(40)

        self.startButtonLayout.addStretch()
        self.startButtonLayout.addWidget(self.startButton)
        self.startButtonLayout.addStretch()

        self.verticalLayout.addLayout(self.startButtonLayout)

        QMetaObject.connectSlotsByName(transcriptionInterface)