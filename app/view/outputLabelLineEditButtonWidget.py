from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy
from qfluentwidgets import LineEdit, ToolButton, CardWidget, TitleLabel, FluentIcon as FIF


class OutputGroupWidget(CardWidget):
    """输出目录设置组件"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi()

    def setupUi(self):
        """设置UI界面"""
        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 16, 20, 16)
        self.mainLayout.setSpacing(10)

        # 标题
        self.titleLabel = TitleLabel(self.tr("输出文件目录"))
        self.mainLayout.addWidget(self.titleLabel)

        # 水平布局
        self.hLayout = QHBoxLayout()
        self.hLayout.setSpacing(8)

        # 提示标签
        self.label = QLabel(self.tr("当前目录为空时将会自动创建相应目录"))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 文本输入框
        self.lineEdit = LineEdit()
        self.lineEdit.setPlaceholderText(self.tr("当目录为空时，将在当前目录下生成相应文件夹存储"))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setToolTip(self.tr("设置音频提取结果输出的目录"))

        # 文件夹按钮
        self.toolButton = ToolButton()
        self.toolButton.setIcon(FIF.FOLDER)
        self.toolButton.setToolTip(self.tr("选择输出目录"))

        # 添加小部件到水平布局
        self.hLayout.addWidget(self.lineEdit)
        self.hLayout.addWidget(self.toolButton)

        # 添加到主布局
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.hLayout)