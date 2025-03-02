from PySide6.QtCore import Qt, QStringListModel, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFileDialog, QListView)
from qfluentwidgets import (PushButton, CardWidget, TitleLabel, FluentIcon as FIF,
                            TransparentPushButton, InfoBar, InfoBarPosition)
import os


class FileNameListView(CardWidget):
    """文件列表视图组件"""

    fileListChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setupUi()
        self.connectSignals()

    def setupUi(self):
        """设置UI界面"""
        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 16, 20, 16)
        self.mainLayout.setSpacing(10)

        # 标题和文件列表标签
        self.titleLabel = TitleLabel(self.tr("音频/视频文件列表"))
        self.mainLayout.addWidget(self.titleLabel)

        # 文件列表部分
        self.listLayout = QHBoxLayout()

        # 列表视图
        self.listView = QListView()
        self.listModel = QStringListModel()
        self.listView.setModel(self.listModel)
        self.listView.setEditTriggers(QListView.NoEditTriggers)
        self.listView.setSelectionMode(QListView.ExtendedSelection)
        self.listLayout.addWidget(self.listView)

        # 按钮部分
        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.setSpacing(10)

        # 添加按钮
        self.addButton = PushButton(self.tr("添加"))
        self.addButton.setIcon(FIF.ADD)
        self.buttonLayout.addWidget(self.addButton)

        # 删除按钮
        self.deleteButton = PushButton(self.tr("删除"))
        self.deleteButton.setIcon(FIF.DELETE)
        self.buttonLayout.addWidget(self.deleteButton)

        # 清空按钮
        self.clearButton = PushButton(self.tr("清空"))
        self.clearButton.setIcon(FIF.REMOVE)
        self.buttonLayout.addWidget(self.clearButton)

        # 添加弹性空间
        self.buttonLayout.addStretch(1)

        # 将按钮布局添加到列表布局
        self.listLayout.addLayout(self.buttonLayout)

        # 将列表布局添加到主布局
        self.mainLayout.addLayout(self.listLayout)

        # 底部显示拖放提示
        self.dropLabel = QLabel(self.tr("或将文件拖放到此处"))
        self.dropLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.dropLabel)

    def connectSignals(self):
        """连接信号和槽"""
        self.addButton.clicked.connect(self.addFiles)
        self.deleteButton.clicked.connect(self.deleteSelectedFiles)
        self.clearButton.clicked.connect(self.clearFiles)

    def addFiles(self):
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr("选择音频/视频文件"),
            "",
            self.tr("音频/视频文件 (*.mp3 *.wav *.flac *.ogg *.aac *.m4a *.mp4 *.avi *.mkv *.mov);;所有文件 (*.*)")
        )

        if not files:
            return

        self.addFilesToList(files)

    def addFilesToList(self, files):
        """将文件添加到列表"""
        current_files = self.listModel.stringList()
        new_files = []

        # 过滤已经存在的文件和不存在的文件
        for file in files:
            if file not in current_files and os.path.isfile(file):
                new_files.append(file)

        if not new_files:
            return

        # 更新列表
        all_files = current_files + new_files
        self.listModel.setStringList(all_files)

        # 发出文件列表变更信号
        self.fileListChanged.emit(all_files)

        # 显示成功提示
        InfoBar.success(
            title=self.tr("添加成功"),
            content=self.tr(f"已添加 {len(new_files)} 个文件"),
            parent=self,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000
        )

    def deleteSelectedFiles(self):
        """删除选中的文件"""
        indexes = self.listView.selectedIndexes()
        if not indexes:
            return

        current_files = self.listModel.stringList()
        selected_rows = [index.row() for index in indexes]

        # 按索引从大到小排序，避免删除后索引变化
        selected_rows.sort(reverse=True)

        # 删除选中的行
        for row in selected_rows:
            current_files.pop(row)

        # 更新列表
        self.listModel.setStringList(current_files)

        # 发出文件列表变更信号
        self.fileListChanged.emit(current_files)

    def clearFiles(self):
        """清空文件列表"""
        self.listModel.setStringList([])

        # 发出文件列表变更信号
        self.fileListChanged.emit([])

    def getFileList(self):
        """获取当前文件列表"""
        return self.listModel.stringList()

    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """拖拽放置事件"""
        if event.mimeData().hasUrls():
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                file_paths.append(file_path)

            self.addFilesToList(file_paths)
            event.acceptProposedAction()
        else:
            event.ignore()