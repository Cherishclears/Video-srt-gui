from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from app.ui.Ui_home import Ui_home

class homeInterface(Ui_home, QWidget):

    # 定义信号，用于切换到其他界面
    navigateToInterface = Signal(str)

    def __init__(self, parent =None):
        super().__init__(parent = parent)  # 如果parent是None，则homeInterface 是一个顶级窗口；如果 parent 是一个控件，则 homeInterface 是该控件的子控件。
        self.setupUi(self)

        # 连接卡片按钮的点击事件
        self.connectSignals()

        # 响应窗口大小变化
        self.resizeCards()


    def connectSignals(self):
        """连接所有卡片按钮的信号"""
        # 为每个按钮连接点击信号
        for i, button in enumerate(self.cardButtons):
            # 获取卡片标题（用于确定导航目标）
            cardTitle = self.cards[i].findChild(QWidget, f"label_{button.objectName()[7:]}").text()

            # 根据卡片标题确定导航目标
            route = self.getRouteFromTitle(cardTitle)

            # 使用lambda捕获当前路由值 (当按钮被点击时会调用该方法onCardButtonClicked)。
            button.clicked.connect(lambda checked=False, r=route: self.onCardButtonClicked(r))


    def getRouteFromTitle(self, title):
        """根据卡片标题确定导航路由"""
        route_map = {
            "视频下载": "download",
            "音频分离": "demucs",
            "加载模型": "model",
            "参数设置": "whisper",
            "转录": "transcription",
            "格式转换": "convert",
            "批量处理": "batch"
        }
        # 返回映射的路由，如果找不到则返回标题的拼音首字母
        return route_map.get(title, title)

    def onCardButtonClicked(self, route):
        """卡片按钮点击处理函数"""
        # 发出导航信号
        self.navigateToInterface.emit(route)

    def addCard(self, title):
        """添加一个新卡片"""
        # 计算当前行和列
        total_cards = len(self.cards)
        row = total_cards // 3
        col = total_cards % 3

        # 创建新卡片
        card = self.createCard(title)

        # 将卡片添加到网格布局
        self.gridLayout.addWidget(card, row, col, 1, 1)

        # 重新连接信号
        self.connectSignals()

    def resizeEvent(self, event):
        """处理窗口大小变化事件"""
        super().resizeEvent(event)
        self.resizeCards()

    def resizeCards(self):
        """根据窗口大小调整卡片宽度"""
        # 计算每个卡片的理想宽度（基于可用宽度）
        availableWidth = self.scrollAreaContents.width() - 30  # 减去边距
        cardWidth = max(200, (availableWidth - 30) // 3)  # 每行3个卡片，减去间距

        # 设置每个卡片的固定高度和首选宽度
        for card in self.cards:
            card.setFixedHeight(220)  # 固定高度
            card.setMinimumWidth(cardWidth)  # 最小宽度