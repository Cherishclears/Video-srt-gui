from PySide6.QtCore import Qt, Signal, QThread, QObject
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from qfluentwidgets import InfoBar, InfoBarPosition, FluentIcon as FIF

import os
import torch
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from torchaudio.transforms import Fade
import torchaudio
import numpy as np

from app.ui.Ui_demucs import Ui_demucs
# from .style_sheet import StyleSheet


class DemucsWorker(QThread):
    """处理音频分离的工作线程"""
    signal_vr_over = Signal(bool)
    file_process_status = Signal(dict)

    def __init__(self, parent, audio_files, stems, model_path, segment=10, overlap=0.1, sample_rate=44100,
                 output_path=""):
        super().__init__(parent)
        self.is_running = False
        self.model_path = model_path
        self.model = None
        self.audio_files = audio_files
        self.sampleRate = sample_rate
        self.segment = segment
        self.overlap = overlap
        self.stems = stems
        self.output_path = output_path

    def run(self):
        self.is_running = True

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"设备: {device}")

        if not self.is_running:
            return

        self.file_process_status.emit({"file": "", "status": False, "task": "加载模型"})
        if self.model is None:
            try:
                self.loadModel(device=device)
            except Exception as e:
                print(f"加载模型出错: \n{str(e)}")
                self.signal_vr_over.emit(False)
                self.stop()
                return

        for audio_file in self.audio_files:
            if not self.is_running:
                break

            self.file_process_status.emit({"file": audio_file, "status": False, "task": "重采样音频"})
            print(f"当前任务: {audio_file}")
            print("重采样音频...")

            try:
                samples = self.load_audio(audio_file, 44100, device=device)
            except Exception as e:
                print(f"重采样音频出错:\n{str(e)}")
                continue

            if not self.is_running:
                break

            print("分离音轨...")
            self.file_process_status.emit({"file": audio_file, "status": False, "task": "分离音轨"})

            try:
                sources = self.separate_sources(
                    self.model,
                    samples[None],
                    self.segment,
                    self.overlap,
                    device,
                    self.sampleRate
                )
            except Exception as e:
                print(f"\n分离音轨出错:\n    {str(e)}")
                continue

            if (sources is None) or (not self.is_running):
                continue

            self.file_process_status.emit({"file": audio_file, "status": False, "task": "保存文件"})
            print("保存文件...")

            try:
                self.save_result(
                    sources=sources,
                    file_path=audio_file,
                    model=self.model,
                    stems=self.stems,
                    output_path=self.output_path
                )

            except Exception as e:
                print(f"保存音频出错:\n{str(e)}")
                continue

            if not self.is_running:
                break

            self.file_process_status.emit({"file": audio_file, "status": True, "task": "处理完成"})
            del samples
            del sources

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        # 处理完成，发送完成信号
        self.signal_vr_over.emit(True)
        print("处理完成!")

        # 清理资源
        del self.model
        self.model = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        self.stop()

    def stop(self):
        self.is_running = False

    def loadModel(self, device=None):
        """加载Demucs模型"""
        # 确保模型目录存在
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        print(f"模型路径: {self.model_path}")

        # 不直接设置模型路径，而是让torchaudio自动处理下载
        bundle = HDEMUCS_HIGH_MUSDB_PLUS

        # 只有当模型文件已存在时才设置路径
        if os.path.exists(self.model_path):
            print("找到已存在的模型文件")
            bundle._model_path = self.model_path
        else:
            print("模型文件不存在，将自动下载")
            # 不设置bundle._model_path，让torchaudio使用默认下载机制

        bundle._sample_rate = 44100
        sample_rate = bundle.sample_rate
        print(f"采样率: {sample_rate}")

        if not self.is_running:
            return

        self.model = bundle.get_model()
        self.model.to(device)

        # 如果模型成功加载，且文件不存在，尝试保存模型到指定路径
        if not os.path.exists(self.model_path) and self.model is not None:
            try:
                # 确保目录存在
                os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
                # 尝试保存模型状态字典
                torch.save(self.model.state_dict(), self.model_path)
                print(f"模型已保存到: {self.model_path}")
            except Exception as e:
                print(f"保存模型失败: {str(e)}")

    def load_audio(self, file_path, sample_rate, device):
        """加载并重采样音频"""
        file_path = os.path.abspath(file_path)

        try:
            # 首先尝试使用torchaudio.load
            waveform, original_sample_rate = torchaudio.load(file_path)
        except Exception as e:
            print(f"使用torchaudio.load加载失败，尝试使用ffmpeg: {str(e)}")
            # 尝试使用ffmpeg作为后备方案
            try:
                import subprocess
                import numpy as np
                from scipy.io import wavfile

                # 创建临时WAV文件
                temp_wav = file_path + ".temp.wav"

                # 使用ffmpeg转换为WAV
                subprocess.call(['ffmpeg', '-i', file_path, '-ar', str(sample_rate), '-ac', '2', temp_wav])

                # 读取转换后的WAV文件
                sr, data = wavfile.read(temp_wav)

                # 确保是立体声
                if len(data.shape) == 1:
                    data = np.column_stack((data, data))

                # 转换为torch张量
                waveform = torch.tensor(data.T, dtype=torch.float32) / 32768.0
                original_sample_rate = sr

                # 删除临时文件
                try:
                    os.remove(temp_wav)
                except:
                    pass
            except Exception as backup_e:
                raise Exception(f"使用torchaudio和ffmpeg都无法加载音频: {str(e)} | {str(backup_e)}")

        # 将单声道转换为立体声
        if waveform.size(0) == 1:
            waveform = torch.cat([waveform, waveform], dim=0)

        # 需要重采样
        if original_sample_rate != sample_rate:
            resampler = torchaudio.transforms.Resample(original_sample_rate, sample_rate)
            waveform = resampler(waveform)

        return waveform

    def separate_sources(self, model, mix, segment=10.0, overlap=0.1, device=None, sample_rate=44100):
        """分离音轨"""
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)

        batch, channels, length = mix.shape

        chunk_len = int(sample_rate * segment * (1 + overlap))
        start = 0
        end = chunk_len
        overlap_frames = overlap * sample_rate
        fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

        final = torch.zeros(batch, len(model.sources), channels, length, device=device)

        while start < length - overlap_frames:
            if not self.is_running:
                return None

            chunk = mix[:, :, start:end]
            # 使用 .to() 方法直接转换数据类型和设备，而不是创建新张量
            chunk = chunk.to(device=device, dtype=torch.float32)

            with torch.no_grad():
                out = model.forward(chunk)

            if not self.is_running:
                return None

            out = fade(out)
            final[:, :, :, start:end] += out
            if start == 0:
                fade.fade_in_len = int(overlap_frames)
                start += int(chunk_len - overlap_frames)
            else:
                start += chunk_len
            end += chunk_len
            if end >= length:
                fade.fade_out_len = 0

            del out
            del chunk
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        return final

    def save_result(self, model, file_path, sources, stems, output_path):
        """保存处理结果到文件"""
        sources_list = model.sources
        print(f"可用音轨: {sources_list}")

        # 将不同输出音轨排列成为列表形式存储
        sources = list(sources[0])

        # 将输出音轨整合为字典形式存储
        audios = dict(zip(sources_list, sources))

        # 获取文件名、文件路径
        data_dir, file_name = os.path.split(file_path)
        file_output = file_name.split(".")
        file_output = ".".join(file_output[:-1])

        # 根据用户选择的不同输出音轨，进行相应处理
        if stems == 0:  # 所有音轨
            stems_to_save = ["vocals", "other", "bass", "drums"]
        elif stems == 1:  # 仅人声
            stems_to_save = ["vocals"]
        elif stems == 2:  # 仅背景声(其它)
            stems_to_save = ["other"]
        elif stems == 3:  # 仅贝斯声
            stems_to_save = ["bass"]
        elif stems == 4:  # 仅鼓点声
            stems_to_save = ["drums"]
        else:  # 人声、背景声二分 (stems == 5)
            stems_to_save = ["vocals", "other"]
            # 合并所有非人声音轨到背景声
            audios["other"] = audios["other"] + audios["bass"] + audios["drums"]

        # 设置输出路径
        if not output_path:
            output_path = os.path.join(data_dir, file_output)
        else:
            output_path = os.path.join(output_path, file_output)

        # 创建输出目录
        if not os.path.exists(output_path):
            print(f"创建输出文件夹: {output_path}")
            os.makedirs(output_path)

        # 保存每个音轨
        for stem in stems_to_save:
            spec = audios[stem][:, :].cpu()
            output_fileName = os.path.join(output_path, f"{file_output}_{stem}.wav")
            print(f"保存文件: {output_fileName}")

            torchaudio.save(output_fileName, spec, self.sampleRate)

class demucsInterface(QWidget, Ui_demucs):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 设置缓存和模型路径
        self.cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "demucs")
        # 确保缓存目录存在
        os.makedirs(self.cache_dir, exist_ok=True)
        self.model_path = os.path.join(self.cache_dir, "models", "hdemucs_high_trained.pt")

        # 初始化工作线程
        self.demucs_worker = None

        # 连接信号
        self.connectSignals()

        # 检查可用设备
        if torch.cuda.is_available():
            print(f"使用GPU: {torch.cuda.get_device_name()}")
        else:
            print("使用CPU (GPU不可用)")

        # 添加警告屏蔽
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning, module="torchaudio.pipelines")

    def connectSignals(self):
        """连接信号和槽"""
        # 连接处理按钮点击事件
        self.process_button.clicked.connect(self.startProcessing)

        # 连接输出目录选择
        self.outputGroupWidget.toolButton.clicked.connect(self.selectOutputDirectory)

    def selectOutputDirectory(self):
        """选择输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            self.tr("选择输出目录"),
            ""
        )

        if directory:
            self.outputGroupWidget.lineEdit.setText(directory)

    def startProcessing(self):
        """开始处理音频文件"""
        # 检查是否有进程正在运行
        if self.demucs_worker and self.demucs_worker.isRunning():
            # 如果有，询问是否取消
            msg_box = QMessageBox.question(
                self,
                self.tr("取消处理"),
                self.tr("是否要取消当前的处理任务?"),
                QMessageBox.Yes | QMessageBox.No
            )

            if msg_box == QMessageBox.Yes:
                self.demucs_worker.stop()
                self.process_button.setText(self.tr("提取"))

            return

        # 检查是否有文件要处理
        files = self.fileListView.getFileList()
        if not files:
            InfoBar.error(
                title=self.tr("错误"),
                content=self.tr("请添加音频文件进行处理"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return

        # 获取参数
        segment = self.spinBox_segment.value()
        overlap = self.spinBox_overlap.value()
        stems = self.comboBox_stems.currentIndex()

        # 获取输出路径
        output_path = self.outputGroupWidget.lineEdit.text()

        # 创建工作线程
        self.demucs_worker = DemucsWorker(
            parent=self,
            audio_files=files,
            stems=stems,
            model_path=self.model_path,
            segment=segment,
            overlap=overlap,
            output_path=output_path
        )

        # 连接信号
        self.demucs_worker.signal_vr_over.connect(self.processingFinished)
        self.demucs_worker.file_process_status.connect(self.updateProcessStatus)

        # 开始处理
        self.demucs_worker.start()
        self.process_button.setText(self.tr("取消"))

    def processingFinished(self, success):
        """处理完成的回调"""
        self.process_button.setText(self.tr("提取"))

        if success:
            InfoBar.success(
                title=self.tr("处理完成"),
                content=self.tr("所有文件处理成功"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
        else:
            InfoBar.error(
                title=self.tr("处理失败"),
                content=self.tr("部分文件处理失败，请查看控制台获取详细信息"),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )

    def updateProcessStatus(self, status_dict):
        """更新处理状态"""
        task = status_dict["task"]
        file = status_dict["file"]

        if file:
            file_name = os.path.basename(file)
            status_text = f"{task}: {file_name}"
        else:
            status_text = task

        # 这里可以添加状态显示逻辑，比如状态栏或进度条
        print(status_text)

    def getParam(self):
        """获取界面参数"""
        param = {}
        param["overlap"] = self.spinBox_overlap.value()
        param["segment"] = self.spinBox_segment.value()
        param["tracks"] = self.comboBox_stems.currentIndex()

        return param

    def setParam(self, param):
        """设置界面参数"""
        try:
            self.spinBox_overlap.setValue(param["overlap"])
            self.spinBox_segment.setValue(param["segment"])
            self.comboBox_stems.setCurrentIndex(param["tracks"])
        except Exception as e:
            print(f"设置参数出错: {str(e)}")