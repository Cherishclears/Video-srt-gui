from PySide6.QtCore import QMetaObject, Qt, QSize
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QFrame)
from qfluentwidgets import (CardWidget, PrimaryPushButton, DoubleSpinBox, ComboBox,
                            LineEdit, PushButton, TitleLabel, BodyLabel, IconWidget,
                            FluentIcon as FIF, TransparentPushButton, ScrollArea)
from ..view.fileNameListViewInterface import FileNameListView
from ..view.outputLabelLineEditButtonWidget import OutputGroupWidget


class Ui_demucs(object):
    def setupUi(self, demucsInterface):
        if not demucsInterface.objectName():
            demucsInterface.setObjectName(u"demucsInterface")

        # 设置主界面垂直布局
        self.verticalLayout = QVBoxLayout(demucsInterface)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(36, 10, 36, 10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setAlignment(Qt.AlignTop)

        # 隐藏模型状态标签
        self.modelStatusVisible = False

        # 创建文件列表视图
        self.fileListView = FileNameListView(demucsInterface)
        self.verticalLayout.addWidget(self.fileListView)

        # 创建Demucs参数卡片
        self.createDemucsParamCard(demucsInterface)

        # 创建输出组件
        self.outputGroupWidget = OutputGroupWidget(demucsInterface)
        self.verticalLayout.addWidget(self.outputGroupWidget)

        # 提取按钮
        self.process_button = PrimaryPushButton(demucsInterface)
        self.process_button.setText(self.tr("提取"))
        self.process_button.setIcon(FIF.IOT)
        self.process_button.setMinimumHeight(36)
        self.verticalLayout.addWidget(self.process_button)

        QMetaObject.connectSlotsByName(demucsInterface)

    def createDemucsParamCard(self, parent):
        """创建Demucs参数设置卡片"""
        self.demucsParamCard = CardWidget(parent)
        self.demucsParamCard.setObjectName(u"demucsParamCard")
        self.demucsParamCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 卡片内布局
        self.paramCardLayout = QVBoxLayout(self.demucsParamCard)
        self.paramCardLayout.setContentsMargins(20, 16, 20, 16)
        self.paramCardLayout.setSpacing(15)

        # 参数标题
        self.paramTitle = TitleLabel(self.tr("Demucs 参数"))
        self.paramCardLayout.addWidget(self.paramTitle)

        # 参数网格布局
        self.paramGridLayout = QHBoxLayout()
        self.paramGridLayout.setSpacing(20)

        # 1. 采样重叠度
        self.overlapLayout = QVBoxLayout()
        self.overlapLabel = BodyLabel(self.tr("采样重叠度"))
        self.spinBox_overlap = DoubleSpinBox()
        self.spinBox_overlap.setRange(0.01, 0.5)
        self.spinBox_overlap.setSingleStep(0.01)
        self.spinBox_overlap.setValue(0.10)
        self.spinBox_overlap.setDecimals(2)
        self.spinBox_overlap.setToolTip(self.tr("分段采样的段间重叠度，该值不宜过小，以免影响分段之间的分离结果的融合度"))

        self.overlapLayout.addWidget(self.overlapLabel)
        self.overlapLayout.addWidget(self.spinBox_overlap)
        self.paramGridLayout.addLayout(self.overlapLayout)

        # 2. 分段长度
        self.segmentLayout = QVBoxLayout()
        self.segmentLabel = BodyLabel(self.tr("分段长度(s)"))
        self.spinBox_segment = DoubleSpinBox()
        self.spinBox_segment.setRange(1, 30)
        self.spinBox_segment.setSingleStep(1)
        self.spinBox_segment.setValue(7.8)
        self.spinBox_segment.setDecimals(1)
        self.spinBox_segment.setToolTip(self.tr("Demucs 是一个极其消耗计算机内存和显存的模型，\n"
                                                "世界上没有任何计算机能够直接使用该模型处理长时音频数据\n"
                                                "因此数据将按照该值所示的秒数，分段处理，值越大将越消耗计算机资源，但效果可能会有提升"))

        self.segmentLayout.addWidget(self.segmentLabel)
        self.segmentLayout.addWidget(self.spinBox_segment)
        self.paramGridLayout.addLayout(self.segmentLayout)

        # 3. 输出音轨
        self.stemsLayout = QVBoxLayout()
        self.stemsLabel = BodyLabel(self.tr("输出音轨"))
        self.comboBox_stems = ComboBox()
        self.comboBox_stems.addItems([
            self.tr("所有音轨"),
            self.tr("仅人声"),
            self.tr("仅背景声"),
            self.tr("仅贝斯声"),
            self.tr("仅鼓点声"),
            self.tr("人声、背景声二分")
        ])
        self.comboBox_stems.setCurrentIndex(1)  # 默认为仅人声

        self.stemsLayout.addWidget(self.stemsLabel)
        self.stemsLayout.addWidget(self.comboBox_stems)
        self.paramGridLayout.addLayout(self.stemsLayout)

        # 添加参数网格到卡片布局
        self.paramCardLayout.addLayout(self.paramGridLayout)

        # 添加卡片到主布局
        self.verticalLayout.addWidget(self.demucsParamCard)

    def tr(self, text):
        return QMetaObject.tr(self, text)