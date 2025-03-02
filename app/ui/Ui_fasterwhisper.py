from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QScrollArea, QFrame, QSizePolicy)
from qfluentwidgets import (TitleLabel, BodyLabel, LineEdit, StrongBodyLabel,
                            ComboBox, SwitchButton, CardWidget, SubtitleLabel,
                            PushButton, FluentIcon as FIF, SmoothScrollArea)


class ParameterCard(CardWidget):
    """A card widget for parameter groups"""

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.contentLayout = QVBoxLayout()

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 16, 16, 16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addLayout(self.contentLayout)

    def addItem(self, label, widget, tooltip=None):
        """Add a parameter item to the card"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create label
        paramLabel = BodyLabel(label, container)
        if tooltip:
            paramLabel.setToolTip(tooltip)

        layout.addWidget(paramLabel)
        layout.addWidget(widget, 1)

        self.contentLayout.addWidget(container)
        return container


class Ui_fasterwhisper(object):
    def setupUi(self, fasterwhisperInterface):
        if not fasterwhisperInterface.objectName():
            fasterwhisperInterface.setObjectName(u"fasterwhisperInterface")

        # Create main layout
        self.mainLayout = QVBoxLayout(fasterwhisperInterface)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area
        self.scrollArea = SmoothScrollArea(fasterwhisperInterface)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create scroll content widget
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName(u"scrollWidget")

        # Create layout for scroll widget
        self.verticalLayout = QVBoxLayout(self.scrollWidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(36, 20, 36, 20)

        # Title and subtitle
        self.titleLabel = TitleLabel(u"FasterWhisper")
        self.subtitleLabel = BodyLabel(u"faster-whisper 模型全部参数")
        self.verticalLayout.addWidget(self.titleLabel)
        self.verticalLayout.addWidget(self.subtitleLabel)

        # === 常规设置 ===
        self.normalCard = ParameterCard(u"常规", self.scrollWidget)

        # 音频语言
        self.languageComboBox = ComboBox(self.normalCard)
        self.normalCard.addItem(u"音频语言", self.languageComboBox,
                                u"音频中的语言。如果选择 Auto，则自动在音频的前30秒内检测语言。")

        # 语言检测阈值
        self.languageThresholdLineEdit = LineEdit(self.normalCard)
        self.languageThresholdLineEdit.setText("0.5")
        self.normalCard.addItem(u"语言检测阈值", self.languageThresholdLineEdit,
                                u"自动检测音频时，语言检测的阈值。如果某种语言的最大概率高于此值，则会检测为该语言。")

        # 语言检测段落数
        self.languageSegmentsLineEdit = LineEdit(self.normalCard)
        self.languageSegmentsLineEdit.setText("1")
        self.normalCard.addItem(u"语言检测段落数", self.languageSegmentsLineEdit,
                                u"自动检测音频时，语言检测需考虑的分段数。")

        # 翻译为英语
        self.translateSwitch = SwitchButton(self.normalCard)
        container = self.normalCard.addItem(u"翻译为英语", self.translateSwitch,
                                            u"输出转写结果翻译为英语的翻译结果")
        container.layout().setAlignment(self.translateSwitch, Qt.AlignLeft)

        # 多语言模式
        self.multilingualSwitch = SwitchButton(self.normalCard)
        container = self.normalCard.addItem(u"多语言模式", self.multilingualSwitch,
                                            u"多语言模式，允许模型处理包含多种语言的音频。")
        container.layout().setAlignment(self.multilingualSwitch, Qt.AlignLeft)

        # 关闭时间戳细分
        self.noTimestampsSwitch = SwitchButton(self.normalCard)
        container = self.normalCard.addItem(u"关闭时间戳细分", self.noTimestampsSwitch,
                                            u"开启时将会输出长文本段落并对应长段落时间戳，不再进行段落细分以及相应的时间戳输出")
        container.layout().setAlignment(self.noTimestampsSwitch, Qt.AlignLeft)

        # 单词级时间戳
        self.wordTimestampsSwitch = SwitchButton(self.normalCard)
        container = self.normalCard.addItem(u"单词级时间戳", self.wordTimestampsSwitch,
                                            u"输出卡拉OK式歌词，支持 SMI VTT LRC 格式")
        container.layout().setAlignment(self.wordTimestampsSwitch, Qt.AlignLeft)

        # 根据说话人聚合内容
        self.aggregateContentsSwitch = SwitchButton(self.normalCard)
        container = self.normalCard.addItem(u"根据说话人聚合内容", self.aggregateContentsSwitch,
                                            u"按顺序将相同说话人的内容聚合到一起，仅支持 txt 格式输出")
        container.layout().setAlignment(self.aggregateContentsSwitch, Qt.AlignLeft)

        self.verticalLayout.addWidget(self.normalCard)

        # === 音频分段设置 ===
        self.audioSegmentsCard = ParameterCard(u"音频分段设置", self.scrollWidget)

        # 最大新令牌数
        self.maxNewTokensLineEdit = LineEdit(self.audioSegmentsCard)
        self.maxNewTokensLineEdit.setText("448")
        self.audioSegmentsCard.addItem(u"最大新令牌数", self.maxNewTokensLineEdit,
                                       u"Whisper 为每个音频块生成的新令牌的最大数量。")

        # 音频块长度
        self.chunkLengthLineEdit = LineEdit(self.audioSegmentsCard)
        self.chunkLengthLineEdit.setText("30")
        self.audioSegmentsCard.addItem(u"音频块长度", self.chunkLengthLineEdit,
                                       u"音频段的长度，默认为 30 秒")

        # 音频分段模式
        self.clipModeComboBox = ComboBox(self.audioSegmentsCard)
        self.clipModeComboBox.addItems([u"不启用手动分段", u"按秒分割", u"按时间戳分割"])
        self.audioSegmentsCard.addItem(u"音频分段模式", self.clipModeComboBox,
                                       u"手动输入音频分段时要使用的分段标记方式,启用的情况下可以输入分段起止时间戳、秒为单位的分段起止点。")

        # 分段时间戳
        self.clipTimestampsLineEdit = LineEdit(self.audioSegmentsCard)
        self.clipTimestampsLineEdit.setEnabled(False)
        self.audioSegmentsCard.addItem(u"分段时间戳", self.clipTimestampsLineEdit,
                                       u"手动输入音频分段，可输入分段时间戳，或者分段的起止秒数点，\n用\"-\"分隔起止点，用\";\"分隔不同段，最后一个结束时间戳默认为音频结尾。")

        self.verticalLayout.addWidget(self.audioSegmentsCard)

        # === 幻听参数 ===
        self.hallucinationCard = ParameterCard(u"幻听参数", self.scrollWidget)

        # 幻听静音阈值
        self.hallucinationThresholdLineEdit = LineEdit(self.hallucinationCard)
        self.hallucinationThresholdLineEdit.setText("0")
        self.hallucinationCard.addItem(u"幻听静音阈值", self.hallucinationThresholdLineEdit,
                                       u"如果开启 单词级时间戳 ，当检测到可能的幻觉时，跳过长于此阈值（以秒为单位）的静默期。")

        # 搜索耐心
        self.patienceLineEdit = LineEdit(self.hallucinationCard)
        self.patienceLineEdit.setText("1.0")
        self.hallucinationCard.addItem(u"搜索耐心", self.patienceLineEdit,
                                       u"搜索音频块时的耐心因子")

        # 惩罚常数
        self.lengthPenaltyLineEdit = LineEdit(self.hallucinationCard)
        self.lengthPenaltyLineEdit.setText("1.0")
        self.hallucinationCard.addItem(u"惩罚常数", self.lengthPenaltyLineEdit,
                                       u"指数形式的长度惩罚常数")

        # gzip 压缩比阈值
        self.compressionRatioLineEdit = LineEdit(self.hallucinationCard)
        self.compressionRatioLineEdit.setText("2.4")
        self.hallucinationCard.addItem(u"gzip 压缩比阈值", self.compressionRatioLineEdit,
                                       u"如果音频的gzip压缩比高于此值，则视为失败。")

        # 采样概率阈值
        self.logProbThresholdLineEdit = LineEdit(self.hallucinationCard)
        self.logProbThresholdLineEdit.setText("-1.0")
        self.hallucinationCard.addItem(u"采样概率阈值", self.logProbThresholdLineEdit,
                                       u"如果采样标记的平均对数概率阈值低于此值，则视为失败")

        # 静音阈值
        self.noSpeechThresholdLineEdit = LineEdit(self.hallucinationCard)
        self.noSpeechThresholdLineEdit.setText("0.6")
        self.hallucinationCard.addItem(u"静音阈值", self.noSpeechThresholdLineEdit,
                                       u"音频段的如果非语音概率高于此值，并且对采样标记的平均对数概率低于阈值，则将该段视为静音。")

        # 循环提示
        self.conditionOnPreviousTextSwitch = SwitchButton(self.hallucinationCard)
        container = self.hallucinationCard.addItem(u"循环提示", self.conditionOnPreviousTextSwitch,
                                                   u"如果启用，则将模型的前一个输出作为下一个音频段的提示;禁用可能会导致文本在段与段之间不一致，\n但模型不太容易陷入失败循环，比如重复循环或时间戳失去同步。")
        container.layout().setAlignment(self.conditionOnPreviousTextSwitch, Qt.AlignLeft)

        # 重复惩罚
        self.repetitionPenaltyLineEdit = LineEdit(self.hallucinationCard)
        self.repetitionPenaltyLineEdit.setText("1.0")
        self.hallucinationCard.addItem(u"重复惩罚", self.repetitionPenaltyLineEdit,
                                       u"对先前输出进行惩罚的分数（防重复），设置值>1以进行惩罚")

        # 禁止重复的ngram大小
        self.noRepeatNgramSizeLineEdit = LineEdit(self.hallucinationCard)
        self.noRepeatNgramSizeLineEdit.setText("0")
        self.hallucinationCard.addItem(u"禁止重复的ngram大小", self.noRepeatNgramSizeLineEdit,
                                       u"如果重复惩罚配置生效，该参数防止程序反复使用此相同长度的语句进行重复检查")

        # 空白抑制
        self.suppressBlankSwitch = SwitchButton(self.hallucinationCard)
        self.suppressBlankSwitch.setChecked(True)
        container = self.hallucinationCard.addItem(u"空白抑制", self.suppressBlankSwitch,
                                                   u"在采样开始时抑制空白输出。")
        container.layout().setAlignment(self.suppressBlankSwitch, Qt.AlignLeft)

        self.verticalLayout.addWidget(self.hallucinationCard)

        # === 性能设置 ===
        self.performanceCard = ParameterCard(u"性能设置", self.scrollWidget)

        # 分块大小
        self.beamSizeLineEdit = LineEdit(self.performanceCard)
        self.beamSizeLineEdit.setText("5")
        self.performanceCard.addItem(u"分块大小", self.beamSizeLineEdit,
                                     u"用于解码的音频块的大小。值越大占用越多计算机性能，速度越慢。但该值也影响转写效果")

        self.verticalLayout.addWidget(self.performanceCard)

        # === 概率分布 ===
        self.temperatureCard = ParameterCard(u"概率分布", self.scrollWidget)

        # 温度回退候选值个数
        self.bestOfLineEdit = LineEdit(self.temperatureCard)
        self.bestOfLineEdit.setText("1")
        self.temperatureCard.addItem(u"温度回退候选值个数", self.bestOfLineEdit,
                                     u"采样时使用非零热度的候选值个数，也即回退配置生效的时的回退次数")

        # 温度候选
        self.temperatureLineEdit = LineEdit(self.temperatureCard)
        self.temperatureLineEdit.setText("0")
        self.temperatureCard.addItem(u"温度候选", self.temperatureLineEdit,
                                     u"温度。用于调整概率分布，从而生成不同的结果，可用于生成深度学习的数据标注。同时\n当程序因为压缩比参数或者采样标记概率参数失败时会依次使用,输入多个值时使用英文逗号分隔")

        # 温度回退提示重置
        self.promptResetOnTemperatureLineEdit = LineEdit(self.temperatureCard)
        self.promptResetOnTemperatureLineEdit.setText("0.5")
        self.temperatureCard.addItem(u"温度回退提示重置", self.promptResetOnTemperatureLineEdit,
                                     u"如果运行中温度回退配置生效，则配置温度回退步骤后，应重置带有先前文本的提示词")

        self.verticalLayout.addWidget(self.temperatureCard)

        # === 其他设置 ===
        self.otherSettingsCard = ParameterCard(u"其他设置", self.scrollWidget)

        # 初始提示词
        self.initialPromptLineEdit = LineEdit(self.otherSettingsCard)
        self.otherSettingsCard.addItem(u"初始提示词", self.initialPromptLineEdit,
                                       u"为第一个音频段提供的可选文本字符串或词元 id 提示词，可迭代项。")

        # 初始文本前缀
        self.prefixLineEdit = LineEdit(self.otherSettingsCard)
        self.otherSettingsCard.addItem(u"初始文本前缀", self.prefixLineEdit,
                                       u"为初始音频段提供的可选文本前缀。")

        # 热词/提示短语
        self.hotwordsLineEdit = LineEdit(self.otherSettingsCard)
        self.hotwordsLineEdit.setPlaceholderText(u"这是一个关于xxx的音频文件......")
        self.otherSettingsCard.addItem(u"热词/提示短语", self.hotwordsLineEdit,
                                       u"为模型提供的热词/提示短语。如果给定了 初始文本前缀 则热词无效。")

        # 特定标记抑制
        self.suppressTokensLineEdit = LineEdit(self.otherSettingsCard)
        self.suppressTokensLineEdit.setText("-1")
        self.otherSettingsCard.addItem(u"特定标记抑制", self.suppressTokensLineEdit,
                                       u"要抑制的标记ID列表。 -1 将抑制模型配置文件 config.json 中定义的默认符号集。")

        # 最晚初始时间戳
        self.maxInitialTimestampLineEdit = LineEdit(self.otherSettingsCard)
        self.maxInitialTimestampLineEdit.setText("1.0")
        self.otherSettingsCard.addItem(u"最晚初始时间戳", self.maxInitialTimestampLineEdit,
                                       u"首个时间戳不能晚于此时间。")

        # 标点向后合并
        self.prependPunctuationsLineEdit = LineEdit(self.otherSettingsCard)
        self.prependPunctuationsLineEdit.setText('"\'¿([{-')
        self.otherSettingsCard.addItem(u"标点向后合并", self.prependPunctuationsLineEdit,
                                       u"如果开启单词级时间戳，则将这些标点符号与下一个单词合并。")

        # 标点向前合并
        self.appendPunctuationsLineEdit = LineEdit(self.otherSettingsCard)
        self.appendPunctuationsLineEdit.setText('"\'.。,，!！?？:：)]}、')
        self.otherSettingsCard.addItem(u"标点向前合并", self.appendPunctuationsLineEdit,
                                       u"如果开启单词级时间戳，则将这些标点符号与前一个单词合并。")

        self.verticalLayout.addWidget(self.otherSettingsCard)

        # Set scroll content
        self.scrollArea.setWidget(self.scrollWidget)
        self.mainLayout.addWidget(self.scrollArea)

        QMetaObject.connectSlotsByName(fasterwhisperInterface)