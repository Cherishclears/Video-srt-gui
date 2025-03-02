from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from app.ui.Ui_fasterwhisper import Ui_fasterwhisper


class FasterWhisperInterface(QWidget, Ui_fasterwhisper):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 初始化Language字典
        self.language_dict = {
            "en": "english",
            "zh": "Simplified Chinese",
            "ja": "japanese",
            "ko": "korean",
            "ru": "russian",
            "es": "spanish",
            "fr": "french",
            "de": "german",
            "it": "italian",
            # 可以继续添加更多语言
        }

        # 初始化界面
        self.initLanguageComboBox()

        # 连接信号
        self.clipModeComboBox.currentIndexChanged.connect(self.setClipTimestampsStatus)

    def initLanguageComboBox(self):
        """初始化语言下拉框"""
        self.languageComboBox.clear()
        self.languageComboBox.addItem("Auto")

        for code, name in self.language_dict.items():
            self.languageComboBox.addItem(f"{code}-{name}")

    def setClipTimestampsStatus(self):
        """设置分段时间戳输入框的状态"""
        if self.clipModeComboBox.currentIndex() == 0:
            self.clipTimestampsLineEdit.setPlaceholderText("")
            self.clipTimestampsLineEdit.setEnabled(False)
        elif self.clipModeComboBox.currentIndex() == 1:
            self.clipTimestampsLineEdit.setPlaceholderText("0.0-10.0;25.0-36.0;......")
            self.clipTimestampsLineEdit.setEnabled(True)
        elif self.clipModeComboBox.currentIndex() == 2:
            self.clipTimestampsLineEdit.setPlaceholderText("00:00:10.0-00:00:20.0;00:00:25.0-00:00:36.0;......")
            self.clipTimestampsLineEdit.setEnabled(True)

    def getParameters(self):
        """获取所有参数设置"""
        params = {}

        # 常规参数
        language_index = self.languageComboBox.currentIndex()
        if language_index == 0:
            params["language"] = None  # Auto
        else:
            params["language"] = self.languageComboBox.currentText().split('-')[0]

        params["language_detection_threshold"] = float(self.languageThresholdLineEdit.text())
        params["language_detection_segments"] = int(self.languageSegmentsLineEdit.text())
        params["task"] = "translate" if self.translateSwitch.isChecked() else "transcribe"
        params["multilingual"] = self.multilingualSwitch.isChecked()
        params["without_timestamps"] = self.noTimestampsSwitch.isChecked()
        params["word_timestamps"] = self.wordTimestampsSwitch.isChecked()
        params["aggregate_contents"] = self.aggregateContentsSwitch.isChecked()

        # 音频分段参数
        params["max_new_tokens"] = int(self.maxNewTokensLineEdit.text())
        params["chunk_length"] = float(self.chunkLengthLineEdit.text())

        # 分段模式和时间戳
        params["clip_mode"] = self.clipModeComboBox.currentIndex()

        clip_timestamps = self.clipTimestampsLineEdit.text()
        if clip_timestamps.strip() and params["clip_mode"] > 0:
            params["clip_timestamps"] = clip_timestamps
        else:
            params["clip_timestamps"] = None

        # 幻听参数
        hallucination_threshold = self.hallucinationThresholdLineEdit.text()
        params["hallucination_silence_threshold"] = float(hallucination_threshold) if hallucination_threshold else 0.0

        params["patience"] = float(self.patienceLineEdit.text())
        params["length_penalty"] = float(self.lengthPenaltyLineEdit.text())
        params["compression_ratio_threshold"] = float(self.compressionRatioLineEdit.text())
        params["log_prob_threshold"] = float(self.logProbThresholdLineEdit.text())
        params["no_speech_threshold"] = float(self.noSpeechThresholdLineEdit.text())
        params["condition_on_previous_text"] = self.conditionOnPreviousTextSwitch.isChecked()
        params["repetition_penalty"] = float(self.repetitionPenaltyLineEdit.text())
        params["no_repeat_ngram_size"] = int(self.noRepeatNgramSizeLineEdit.text())
        params["suppress_blank"] = self.suppressBlankSwitch.isChecked()

        # 性能参数
        params["beam_size"] = int(self.beamSizeLineEdit.text())

        # 温度参数
        params["best_of"] = int(self.bestOfLineEdit.text())

        # 处理temperature可能是逗号分隔的列表
        temp_text = self.temperatureLineEdit.text()
        if ',' in temp_text:
            temps = [float(t.strip()) for t in temp_text.split(',')]
            params["temperature"] = temps
        else:
            params["temperature"] = float(temp_text)

        params["prompt_reset_on_temperature"] = float(self.promptResetOnTemperatureLineEdit.text())

        # 其他参数
        params["initial_prompt"] = self.initialPromptLineEdit.text() if self.initialPromptLineEdit.text() else None
        params["prefix"] = self.prefixLineEdit.text() if self.prefixLineEdit.text() else None
        params["hotwords"] = self.hotwordsLineEdit.text() if self.hotwordsLineEdit.text() else None

        # 处理可能是逗号分隔的列表
        suppress_tokens_text = self.suppressTokensLineEdit.text()
        if suppress_tokens_text == "-1":
            params["suppress_tokens"] = [-1]
        elif ',' in suppress_tokens_text:
            params["suppress_tokens"] = [int(t.strip()) for t in suppress_tokens_text.split(',')]
        else:
            params["suppress_tokens"] = [int(suppress_tokens_text)]

        params["max_initial_timestamp"] = float(self.maxInitialTimestampLineEdit.text())
        params["prepend_punctuations"] = self.prependPunctuationsLineEdit.text()
        params["append_punctuations"] = self.appendPunctuationsLineEdit.text()

        return params

    def setParameters(self, params):
        """设置所有参数"""
        # 常规参数
        if params.get("language") is None:
            self.languageComboBox.setCurrentIndex(0)  # Auto
        else:
            for i in range(self.languageComboBox.count()):
                text = self.languageComboBox.itemText(i)
                if text.startswith(params["language"] + "-"):
                    self.languageComboBox.setCurrentIndex(i)
                    break

        self.languageThresholdLineEdit.setText(str(params.get("language_detection_threshold", 0.5)))
        self.languageSegmentsLineEdit.setText(str(params.get("language_detection_segments", 1)))
        self.translateSwitch.setChecked(params.get("task") == "translate")
        self.multilingualSwitch.setChecked(params.get("multilingual", False))
        self.noTimestampsSwitch.setChecked(params.get("without_timestamps", False))
        self.wordTimestampsSwitch.setChecked(params.get("word_timestamps", False))
        self.aggregateContentsSwitch.setChecked(params.get("aggregate_contents", False))

        # 音频分段参数
        self.maxNewTokensLineEdit.setText(str(params.get("max_new_tokens", 448)))
        self.chunkLengthLineEdit.setText(str(params.get("chunk_length", 30)))

        # 分段模式和时间戳
        self.clipModeComboBox.setCurrentIndex(params.get("clip_mode", 0))

        if params.get("clip_timestamps"):
            self.clipTimestampsLineEdit.setText(params["clip_timestamps"])

        # 幻听参数
        if "hallucination_silence_threshold" in params:
            self.hallucinationThresholdLineEdit.setText(str(params["hallucination_silence_threshold"]))

        self.patienceLineEdit.setText(str(params.get("patience", 1.0)))
        self.lengthPenaltyLineEdit.setText(str(params.get("length_penalty", 1.0)))
        self.compressionRatioLineEdit.setText(str(params.get("compression_ratio_threshold", 2.4)))
        self.logProbThresholdLineEdit.setText(str(params.get("log_prob_threshold", -1.0)))
        self.noSpeechThresholdLineEdit.setText(str(params.get("no_speech_threshold", 0.6)))
        self.conditionOnPreviousTextSwitch.setChecked(params.get("condition_on_previous_text", False))
        self.repetitionPenaltyLineEdit.setText(str(params.get("repetition_penalty", 1.0)))
        self.noRepeatNgramSizeLineEdit.setText(str(params.get("no_repeat_ngram_size", 0)))
        self.suppressBlankSwitch.setChecked(params.get("suppress_blank", True))

        # 性能参数
        self.beamSizeLineEdit.setText(str(params.get("beam_size", 5)))

        # 温度参数
        self.bestOfLineEdit.setText(str(params.get("best_of", 1)))

        # 处理temperature可能是列表
        temp = params.get("temperature", 0)
        if isinstance(temp, list):
            self.temperatureLineEdit.setText(','.join(str(t) for t in temp))
        else:
            self.temperatureLineEdit.setText(str(temp))

        self.promptResetOnTemperatureLineEdit.setText(str(params.get("prompt_reset_on_temperature", 0.5)))

        # 其他参数
        if params.get("initial_prompt"):
            self.initialPromptLineEdit.setText(params["initial_prompt"])

        if params.get("prefix"):
            self.prefixLineEdit.setText(params["prefix"])

        if params.get("hotwords"):
            self.hotwordsLineEdit.setText(params["hotwords"])

        # 处理suppress_tokens可能是列表
        suppress_tokens = params.get("suppress_tokens", [-1])
        if suppress_tokens:
            self.suppressTokensLineEdit.setText(','.join(str(t) for t in suppress_tokens))

        self.maxInitialTimestampLineEdit.setText(str(params.get("max_initial_timestamp", 1.0)))

        if "prepend_punctuations" in params:
            self.prependPunctuationsLineEdit.setText(params["prepend_punctuations"])

        if "append_punctuations" in params:
            self.appendPunctuationsLineEdit.setText(params["append_punctuations"])

        # 更新分段输入框的状态
        self.setClipTimestampsStatus()