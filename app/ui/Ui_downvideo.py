from PySide6.QtCore import QSize, Qt, QMetaObject
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QFrame)
from qfluentwidgets import (CardWidget, PrimaryPushButton, StrongBodyLabel,
                            BodyLabel, LineEdit, ComboBox, ProgressBar,
                            PushButton, InfoBar, InfoBarPosition, TransparentPushButton,
                            TitleLabel, SubtitleLabel, IconWidget, FluentIcon as FIF,
                            HyperlinkButton, ToolTipFilter, ToolTipPosition, setTheme, Theme)


class Ui_downvideo(object):
    def setupUi(self, downvideoInterface):
        if not downvideoInterface.objectName():
            downvideoInterface.setObjectName(u"downvideoInterface")

        # 设置主界面的垂直布局
        self.verticalLayout = QVBoxLayout(downvideoInterface)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setAlignment(Qt.AlignTop)  # 设置顶部对齐

        # 创建标题区域
        self.headerLayout = QHBoxLayout()
        self.titleIcon = IconWidget(FIF.DOWN, downvideoInterface)
        self.titleIcon.setFixedSize(36, 36)

        self.titleArea = QVBoxLayout()
        self.titleArea.setSpacing(0)

        self.titleLabel = TitleLabel("视频下载")
        self.subtitleLabel = BodyLabel("下载各种网站的视频到本地")

        self.titleArea.addWidget(self.titleLabel)
        self.titleArea.addWidget(self.subtitleLabel)

        self.headerLayout.addWidget(self.titleIcon)
        self.headerLayout.addLayout(self.titleArea)
        self.headerLayout.addStretch()

        self.verticalLayout.addLayout(self.headerLayout)

        # 创建分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        self.verticalLayout.addWidget(self.separator)

        # 创建主要卡片
        self.mainCard = CardWidget(downvideoInterface)
        self.mainCard.setObjectName(u"mainCard")
        self.mainCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 卡片内部布局
        self.cardLayout = QVBoxLayout(self.mainCard)
        self.cardLayout.setSpacing(20)
        self.cardLayout.setContentsMargins(24, 24, 24, 24)
        self.cardLayout.setAlignment(Qt.AlignTop)  # 设置顶部对齐

        # URL 输入
        self.urlLayout = QVBoxLayout()
        self.urlLayout.setSpacing(6)

        self.urlLabel = SubtitleLabel("视频URL")
        self.urlInput = LineEdit()
        self.urlInput.setPlaceholderText("请输入视频链接")
        self.urlInput.setClearButtonEnabled(True)
        self.urlInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.urlInput.setFixedHeight(36)  # 设置固定高度

        self.urlLayout.addWidget(self.urlLabel)
        self.urlLayout.addWidget(self.urlInput)
        self.cardLayout.addLayout(self.urlLayout)

        # Cookies 文件选择
        self.cookiesLayout = QVBoxLayout()
        self.cookiesLayout.setSpacing(6)

        self.cookiesLabel = SubtitleLabel("Cookies文件 (可选)")

        self.cookiesHLayout = QHBoxLayout()
        self.cookiesPathLabel = LineEdit()
        self.cookiesPathLabel.setReadOnly(True)
        self.cookiesPathLabel.setPlaceholderText("未选择 (对于需要登录的网站可能需要)")
        self.cookiesPathLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cookiesPathLabel.setFixedHeight(36)  # 设置固定高度

        self.cookiesButton = PushButton("选择文件")
        self.cookiesButton.setIcon(FIF.DOCUMENT)
        self.cookiesButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.cookiesButton.setFixedHeight(36)  # 设置固定高度

        self.cookiesHLayout.addWidget(self.cookiesPathLabel)
        self.cookiesHLayout.addWidget(self.cookiesButton)

        self.cookiesLayout.addWidget(self.cookiesLabel)
        self.cookiesLayout.addLayout(self.cookiesHLayout)
        self.cardLayout.addLayout(self.cookiesLayout)

        # 查询按钮
        self.queryButtonLayout = QHBoxLayout()
        self.queryButtonLayout.setContentsMargins(0, 10, 0, 10)

        self.queryButton = PrimaryPushButton("查询视频信息")
        self.queryButton.setFixedHeight(36)
        self.queryButton.setIcon(FIF.SEARCH)

        self.queryButtonLayout.addStretch()
        self.queryButtonLayout.addWidget(self.queryButton)
        self.queryButtonLayout.addStretch()

        self.cardLayout.addLayout(self.queryButtonLayout)

        # 添加分隔线
        self.infoSeparator = QFrame()
        self.infoSeparator.setFrameShape(QFrame.HLine)
        self.infoSeparator.setFrameShadow(QFrame.Sunken)
        self.infoSeparator.setFixedHeight(1)
        self.infoSeparator.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        self.cardLayout.addWidget(self.infoSeparator)

        # 视频信息卡片
        self.infoCard = CardWidget(self.mainCard)
        self.infoCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 改为固定高度策略
        self.infoCard.setFixedHeight(250)  # 设置固定高度

        self.infoCardLayout = QVBoxLayout(self.infoCard)
        self.infoCardLayout.setSpacing(12)
        self.infoCardLayout.setContentsMargins(20, 15, 20, 15)
        self.infoCardLayout.setAlignment(Qt.AlignTop)  # 设置顶部对齐

        # 视频信息显示
        self.infoLabel = SubtitleLabel("视频信息")
        self.videoTitleLabel = BodyLabel("视频标题: ")
        self.videoTitleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.infoCardLayout.addWidget(self.infoLabel)
        self.infoCardLayout.addWidget(self.videoTitleLabel)

        # 格式选择
        self.formatLayout = QVBoxLayout()
        self.formatLayout.setSpacing(6)

        self.formatLabel = SubtitleLabel("选择画质")
        self.formatCombo = ComboBox()
        self.formatCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.formatCombo.setFixedHeight(36)  # 设置固定高度

        self.formatLayout.addWidget(self.formatLabel)
        self.formatLayout.addWidget(self.formatCombo)
        self.infoCardLayout.addLayout(self.formatLayout)

        # 输出路径
        self.outputLayout = QVBoxLayout()
        self.outputLayout.setSpacing(6)

        self.outputLabel = SubtitleLabel("保存路径")

        self.outputHLayout = QHBoxLayout()
        self.outputPathLabel = LineEdit()
        self.outputPathLabel.setReadOnly(True)
        self.outputPathLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.outputPathLabel.setFixedHeight(36)  # 设置固定高度

        self.outputButton = PushButton("更改路径")
        self.outputButton.setIcon(FIF.FOLDER)
        self.outputButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.outputButton.setFixedHeight(36)  # 设置固定高度

        self.outputHLayout.addWidget(self.outputPathLabel)
        self.outputHLayout.addWidget(self.outputButton)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputHLayout)
        self.infoCardLayout.addLayout(self.outputLayout)

        # 添加信息卡片到主卡片
        self.cardLayout.addWidget(self.infoCard)

        # 下载按钮
        self.downloadButtonLayout = QHBoxLayout()
        self.downloadButtonLayout.setContentsMargins(0, 10, 0, 10)

        self.downloadButton = PrimaryPushButton("开始下载")
        self.downloadButton.setFixedHeight(36)
        self.downloadButton.setIcon(FIF.DOWNLOAD)
        self.downloadButton.setEnabled(False)

        self.downloadButtonLayout.addStretch()
        self.downloadButtonLayout.addWidget(self.downloadButton)
        self.downloadButtonLayout.addStretch()

        self.cardLayout.addLayout(self.downloadButtonLayout)

        # 进度条
        self.progressLayout = QVBoxLayout()
        self.progressLayout.setSpacing(8)

        self.progressBar = ProgressBar()
        self.progressBar.setFixedHeight(6)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.statusLabel = BodyLabel("准备就绪")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.progressLayout.addWidget(self.progressBar)
        self.progressLayout.addWidget(self.statusLabel)
        self.cardLayout.addLayout(self.progressLayout)

        # 添加帮助链接
        self.helpLayout = QHBoxLayout()
        self.helpLayout.setContentsMargins(0, 10, 0, 0)

        self.helpLink = HyperlinkButton(
            "https://github.com/yt-dlp/yt-dlp#supported-sites",
            "支持的网站列表",
            self.mainCard,
            FIF.LINK
        )

        self.helpLayout.addStretch()
        self.helpLayout.addWidget(self.helpLink)

        self.cardLayout.addLayout(self.helpLayout)

        # 添加卡片到主布局
        self.verticalLayout.addWidget(self.mainCard)

        # 添加工具提示
        self.urlInput.installEventFilter(ToolTipFilter(
            self.urlInput,
            "输入需要下载的视频链接",
            ToolTipPosition.TOP
        ))

        self.cookiesButton.installEventFilter(ToolTipFilter(
            self.cookiesButton,
            "对于需要登录的网站，您可能需要提供cookies文件",
            ToolTipPosition.TOP
        ))

        self.queryButton.installEventFilter(ToolTipFilter(
            self.queryButton,
            "获取视频信息和可用画质",
            ToolTipPosition.TOP
        ))

        self.formatCombo.installEventFilter(ToolTipFilter(
            self.formatCombo,
            "选择下载画质，'最佳质量'会自动选择最高画质",
            ToolTipPosition.RIGHT
        ))

        # 设置初始大小
        downvideoInterface.setMinimumSize(QSize(700, 780))  # 增加最小高度

        QMetaObject.connectSlotsByName(downvideoInterface)