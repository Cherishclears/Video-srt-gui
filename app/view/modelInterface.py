from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtGui import QFont
from qfluentwidgets import InfoBar, InfoBarPosition, FluentIcon as FIF

from app.ui.Ui_model import Ui_model
from faster_whisper import WhisperModel
import torch
import os


class LoadModelWorker(QThread):
    setStatusSignal = Signal(bool)
    loadModelOverSignal = Signal(bool)

    def __init__(self, modelParam, use_v3_model=False, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.model_size_or_path = modelParam["model_size_or_path"]
        self.device = modelParam["device"]
        self.device_index = modelParam["device_index"]
        self.compute_type = modelParam["compute_type"]
        self.cpu_threads = modelParam["cpu_threads"]
        self.num_workers = modelParam["num_workers"]
        self.use_v3_model = use_v3_model

        self.model = None

    def run(self) -> None:
        self.isRunning = True

        try:
            self.model = WhisperModel(
                model_size_or_path=self.model_size_or_path,
                device=self.device,
                device_index=self.device_index,
                compute_type=self.compute_type,
                cpu_threads=self.cpu_threads,
                num_workers=self.num_workers
            )

            if self.use_v3_model:
                print("\n[Using V3 model, modify number of mel-filters to 128]")
                self.model.feature_extractor.mel_filters = self.model.feature_extractor.get_mel_filters(
                    self.model.feature_extractor.sampling_rate,
                    self.model.feature_extractor.n_fft,
                    n_mels=128
                )

            print("\nLoad over")
            print(self.model_size_or_path)
            print(f"{'max_length: ':23}", self.model.max_length)
            print(f"{'num_samples_per_token: ':23}", self.model.num_samples_per_token)
            print("time_precision: ", self.model.time_precision)
            print("tokens_per_second: ", self.model.tokens_per_second)
            print("input_stride: ", self.model.input_stride)

            self.setStatusSignal.emit(True)
            self.loadModelOverSignal.emit(True)
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.setStatusSignal.emit(False)
            self.loadModelOverSignal.emit(False)

        self.isRunning = False

    def stop(self):
        self.isRunning = False


class modelInterface(QWidget, Ui_model):
    modelLoaded = Signal(WhisperModel)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.model = None
        self.load_model_worker = None

        # 信号连接
        self.connectSignals()

    def connectSignals(self):
        self.modelLocalRadioButton.toggled.connect(self.setModelLocationLayout)
        self.modelPathButton.clicked.connect(self.selectModelPath)
        self.loadModelButton.clicked.connect(self.loadModel)

    def setModelLocationLayout(self):
        # 设置本地模型相关控件的启用状态
        for widget in [self.modelPathLabel, self.modelPathLineEdit, self.modelPathButton]:
            widget.setEnabled(self.modelLocalRadioButton.isChecked())

    def selectModelPath(self):
        model_path = QFileDialog.getExistingDirectory(self, "选择模型目录")
        if model_path:
            self.modelPathLineEdit.setText(model_path)

    def loadModel(self):
        if self.load_model_worker and self.load_model_worker.isRunning:
            return

        # 检查模型路径
        model_path = self.modelPathLineEdit.text().strip()
        if not model_path:
            InfoBar.error(
                title="错误",
                content="请先选择模型路径",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
            return

        if not os.path.exists(model_path):
            InfoBar.error(
                title="错误",
                content="模型路径不存在",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
            return

        # 禁用加载按钮
        self.loadModelButton.setEnabled(False)
        self.loadModelButton.setText("加载中...")

        # 获取参数
        device = self.deviceComboBox.currentText()

        # 解析设备索引
        device_index_text = self.deviceIndexLineEdit.text().strip()
        try:
            if ',' in device_index_text:
                device_index = [int(idx.strip()) for idx in device_index_text.split(',')]
            else:
                device_index = int(device_index_text)
        except ValueError:
            InfoBar.error(
                title="错误",
                content="设备索引格式错误",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
            self.loadModelButton.setEnabled(True)
            self.loadModelButton.setText("加载模型")
            return

        compute_type = self.computeTypeComboBox.currentText()

        # 解析CPU线程数
        try:
            cpu_threads = int(self.cpuThreadsLineEdit.text())
        except ValueError:
            InfoBar.error(
                title="错误",
                content="CPU线程数必须是整数",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
            self.loadModelButton.setEnabled(True)
            self.loadModelButton.setText("加载模型")
            return

        # 解析并发数
        try:
            num_workers = int(self.numWorkersLineEdit.text())
        except ValueError:
            InfoBar.error(
                title="错误",
                content="并发数必须是整数",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
            self.loadModelButton.setEnabled(True)
            self.loadModelButton.setText("加载模型")
            return

        # 是否使用v3模型
        use_v3_model = self.useV3Switch.isChecked()

        # 模型参数
        model_param = {
            "model_size_or_path": model_path,
            "device": device,
            "device_index": device_index,
            "compute_type": compute_type,
            "cpu_threads": cpu_threads,
            "num_workers": num_workers,
        }

        # 创建加载模型的工作线程
        self.load_model_worker = LoadModelWorker(model_param, use_v3_model, self)
        self.load_model_worker.setStatusSignal.connect(self.updateModelStatus)
        self.load_model_worker.loadModelOverSignal.connect(self.onModelLoaded)
        self.load_model_worker.start()

    def updateModelStatus(self, success):
        if success:
            self.modelNotLoadedLabel.setText("模型已加载!")
            self.modelStatusIconLabel.setStyleSheet("background-color: green; border-radius: 12px;")
        else:
            self.modelNotLoadedLabel.setText("模型加载失败!")
            self.modelStatusIconLabel.setStyleSheet("background-color: red; border-radius: 12px;")
            self.loadModelButton.setEnabled(True)
            self.loadModelButton.setText("加载模型")

    def onModelLoaded(self, success):
        self.loadModelButton.setEnabled(True)
        self.loadModelButton.setText("加载模型")

        if success:
            self.model = self.load_model_worker.model
            self.modelLoaded.emit(self.model)

            InfoBar.success(
                title="成功",
                content="模型加载成功",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )
        else:
            InfoBar.error(
                title="错误",
                content="模型加载失败",
                parent=self,
                duration=2000,
                position=InfoBarPosition.TOP
            )