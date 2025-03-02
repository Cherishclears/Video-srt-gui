from PySide6.QtCore import QSize, Qt, QMetaObject
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QRadioButton, QLabel, QFrame)
from PySide6.QtGui import QFont
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel, LineEdit,
                            ComboBox, SwitchButton, PrimaryPushButton, RadioButton,
                            ToolButton, FluentIcon as FIF, CardWidget,
                            StrongBodyLabel, CaptionLabel, HorizontalSeparator)
from qfluentwidgets import InfoBar, InfoBarPosition


class Ui_model(object):
    def setupUi(self, modelInterface):
        if not modelInterface.objectName():
            modelInterface.setObjectName(u"modelInterface")

        # 主布局
        self.verticalLayout = QVBoxLayout(modelInterface)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setContentsMargins(36, 36, 36, 36)

        # 标题部分
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setSpacing(8)

        self.titleLabel = TitleLabel(u"Model")
        self.titleLabel.setObjectName(u"titleLabel")
        self.headerLayout.addWidget(self.titleLabel)

        self.subtitleLabel = SubtitleLabel(u"加载本地模型或下载模型")
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.headerLayout.addWidget(self.subtitleLabel)

        self.verticalLayout.addLayout(self.headerLayout)
        self.verticalLayout.addSpacing(20)

        # 模型状态卡片
        self.statusCard = CardWidget()
        self.statusCard.setObjectName(u"statusCard")
        self.statusCardLayout = QHBoxLayout(self.statusCard)
        self.statusCardLayout.setContentsMargins(20, 16, 20, 16)

        self.modelStatusIconLabel = QLabel()
        self.modelStatusIconLabel.setObjectName(u"modelStatusIconLabel")
        self.modelStatusIconLabel.setMinimumSize(24, 24)
        self.modelStatusIconLabel.setMaximumSize(24, 24)
        self.modelStatusIconLabel.setStyleSheet("background-color: red; border-radius: 12px;")
        self.statusCardLayout.addWidget(self.modelStatusIconLabel)

        self.statusCardLayout.addSpacing(10)

        self.modelNotLoadedLabel = StrongBodyLabel(u"模型未加载!")
        self.modelNotLoadedLabel.setObjectName(u"modelNotLoadedLabel")
        font = QFont()
        font.setBold(True)
        self.modelNotLoadedLabel.setFont(font)
        self.statusCardLayout.addWidget(self.modelNotLoadedLabel)

        self.statusCardLayout.addStretch()

        # 加载模型按钮
        self.loadModelButton = PrimaryPushButton(u"加载模型")
        self.loadModelButton.setObjectName(u"loadModelButton")
        self.loadModelButton.setIcon(FIF.PLAY)
        self.loadModelButton.setFixedSize(160, 44)
        buttonFont = QFont("Segoe UI", 12)
        buttonFont.setBold(True)
        self.loadModelButton.setFont(buttonFont)
        self.statusCardLayout.addWidget(self.loadModelButton)

        self.verticalLayout.addWidget(self.statusCard)
        self.verticalLayout.addSpacing(24)

        # 模型选择部分 - 使用卡片式设计
        self.modelSourceCard = CardWidget()
        self.modelSourceCard.setObjectName(u"modelSourceCard")
        self.modelSourceLayout = QVBoxLayout(self.modelSourceCard)
        self.modelSourceLayout.setContentsMargins(20, 16, 20, 20)
        self.modelSourceLayout.setSpacing(16)

        # 卡片标题
        self.modelSourceTitle = StrongBodyLabel(u"模型来源")
        self.modelSourceTitle.setObjectName(u"modelSourceTitle")
        self.modelSourceLayout.addWidget(self.modelSourceTitle)

        # 分隔线
        self.modelSourceSeparator = HorizontalSeparator()
        self.modelSourceLayout.addWidget(self.modelSourceSeparator)
        self.modelSourceLayout.addSpacing(4)

        # 使用本地模型选项
        self.modelLocalRadioButton = RadioButton(u"使用本地模型")
        self.modelLocalRadioButton.setObjectName(u"modelLocalRadioButton")
        self.modelLocalRadioButton.setChecked(True)
        self.modelSourceLayout.addWidget(self.modelLocalRadioButton)

        # 本地模型路径选择
        self.localModelLayout = QHBoxLayout()
        self.localModelLayout.setSpacing(10)

        self.modelPathLabel = BodyLabel(u"模型目录")
        self.modelPathLabel.setObjectName(u"modelPathLabel")
        self.modelPathLabel.setFixedWidth(80)

        self.modelPathLineEdit = LineEdit()
        self.modelPathLineEdit.setObjectName(u"modelPathLineEdit")
        self.modelPathLineEdit.setClearButtonEnabled(True)
        self.modelPathLineEdit.setPlaceholderText(u"选择本地模型的目录路径")

        self.modelPathButton = ToolButton()
        self.modelPathButton.setObjectName(u"modelPathButton")
        self.modelPathButton.setIcon(FIF.FOLDER)
        self.modelPathButton.setFixedSize(32, 32)

        self.localModelLayout.addWidget(self.modelPathLabel)
        self.localModelLayout.addWidget(self.modelPathLineEdit, 1)
        self.localModelLayout.addWidget(self.modelPathButton)

        self.modelSourceLayout.addLayout(self.localModelLayout)
        self.modelSourceLayout.addSpacing(8)

        # 在线下载模型选项
        self.modelOnlineRadioButton = RadioButton(u"在线下载模型")
        self.modelOnlineRadioButton.setObjectName(u"modelOnlineRadioButton")
        self.modelOnlineRadioButton.setEnabled(False)
        self.modelSourceLayout.addWidget(self.modelOnlineRadioButton)

        self.verticalLayout.addWidget(self.modelSourceCard)
        self.verticalLayout.addSpacing(24)

        # 模型参数设置部分 - 使用卡片式设计
        self.modelParamsCard = CardWidget()
        self.modelParamsCard.setObjectName(u"modelParamsCard")
        self.modelParamsLayout = QVBoxLayout(self.modelParamsCard)
        self.modelParamsLayout.setContentsMargins(20, 16, 20, 20)
        self.modelParamsLayout.setSpacing(16)

        # 卡片标题
        self.modelParamsTitle = StrongBodyLabel(u"模型参数")
        self.modelParamsTitle.setObjectName(u"modelParamsTitle")
        self.modelParamsLayout.addWidget(self.modelParamsTitle)

        # 分隔线
        self.modelParamsSeparator = HorizontalSeparator()
        self.modelParamsLayout.addWidget(self.modelParamsSeparator)
        self.modelParamsLayout.addSpacing(8)

        # 使用网格布局来排列参数
        self.paramsGridLayout = QGridLayout()
        self.paramsGridLayout.setHorizontalSpacing(20)
        self.paramsGridLayout.setVerticalSpacing(16)

        # 使用v3模型
        self.useV3Label = BodyLabel(u"使用 v3 模型")
        self.useV3Label.setObjectName(u"useV3Label")
        self.useV3Switch = SwitchButton()
        self.useV3Switch.setObjectName(u"useV3Switch")
        self.useV3Switch.setOnText(u"v3 模型")
        self.useV3Switch.setOffText(u"非 V3 模型")
        self.paramsGridLayout.addWidget(self.useV3Label, 0, 0)
        self.paramsGridLayout.addWidget(self.useV3Switch, 0, 1)

        # 处理设备
        self.deviceLabel = BodyLabel(u"处理设备")
        self.deviceLabel.setObjectName(u"deviceLabel")
        self.deviceComboBox = ComboBox()
        self.deviceComboBox.setObjectName(u"deviceComboBox")
        self.deviceComboBox.addItems([u"cpu", u"cuda", u"auto"])
        self.deviceComboBox.setCurrentIndex(1)
        self.paramsGridLayout.addWidget(self.deviceLabel, 1, 0)
        self.paramsGridLayout.addWidget(self.deviceComboBox, 1, 1)

        # 设备号
        self.deviceIndexLabel = BodyLabel(u"设备号")
        self.deviceIndexLabel.setObjectName(u"deviceIndexLabel")
        self.deviceIndexLineEdit = LineEdit()
        self.deviceIndexLineEdit.setObjectName(u"deviceIndexLineEdit")
        self.deviceIndexLineEdit.setText("0")
        self.deviceIndexLineEdit.setToolTip(u"要使用的设备ID。也可以通过传递ID列表(例如0,1,2,3)在多GPU上加载模型。")
        self.paramsGridLayout.addWidget(self.deviceIndexLabel, 2, 0)
        self.paramsGridLayout.addWidget(self.deviceIndexLineEdit, 2, 1)

        # 计算精度
        self.computeTypeLabel = BodyLabel(u"计算精度")
        self.computeTypeLabel.setObjectName(u"computeTypeLabel")
        self.computeTypeComboBox = ComboBox()
        self.computeTypeComboBox.setObjectName(u"computeTypeComboBox")
        self.computeTypeComboBox.addItems([u"int8", u"int8_float16", u"int8_bfloat16",
                                           u"int16", u"float16", u"float32", u"bfloat16"])
        self.computeTypeComboBox.setCurrentIndex(5)
        self.computeTypeComboBox.setToolTip(
            u"要使用的计算精度，尽管某些设备不支持半精度，\n但事实上不论选择什么精度类型都可以隐式转换。")
        self.paramsGridLayout.addWidget(self.computeTypeLabel, 0, 2)
        self.paramsGridLayout.addWidget(self.computeTypeComboBox, 0, 3)

        # 线程数（CPU）
        self.cpuThreadsLabel = BodyLabel(u"线程数（CPU）")
        self.cpuThreadsLabel.setObjectName(u"cpuThreadsLabel")
        self.cpuThreadsLineEdit = LineEdit()
        self.cpuThreadsLineEdit.setObjectName(u"cpuThreadsLineEdit")
        self.cpuThreadsLineEdit.setText("4")
        self.cpuThreadsLineEdit.setToolTip(u"在CPU上运行时使用的线程数(默认为4)。")
        self.paramsGridLayout.addWidget(self.cpuThreadsLabel, 1, 2)
        self.paramsGridLayout.addWidget(self.cpuThreadsLineEdit, 1, 3)

        # 并发数
        self.numWorkersLabel = BodyLabel(u"并发数")
        self.numWorkersLabel.setObjectName(u"numWorkersLabel")
        self.numWorkersLineEdit = LineEdit()
        self.numWorkersLineEdit.setObjectName(u"numWorkersLineEdit")
        self.numWorkersLineEdit.setText("1")
        self.numWorkersLineEdit.setToolTip(
            u"具有多个工作线程可以在运行模型时实现真正的并行性。\n这可以以增加内存使用为代价提高整体吞吐量。")
        self.paramsGridLayout.addWidget(self.numWorkersLabel, 2, 2)
        self.paramsGridLayout.addWidget(self.numWorkersLineEdit, 2, 3)

        # 添加到布局
        self.modelParamsLayout.addLayout(self.paramsGridLayout)

        # 附加说明
        self.paramDescriptionLabel = CaptionLabel(
            u"注意：模型加载会占用较多系统资源，请确保您的计算机有足够的内存和计算能力。")
        self.paramDescriptionLabel.setObjectName(u"paramDescriptionLabel")
        self.modelParamsLayout.addWidget(self.paramDescriptionLabel)

        self.verticalLayout.addWidget(self.modelParamsCard)
        self.verticalLayout.addStretch()

        QMetaObject.connectSlotsByName(modelInterface)