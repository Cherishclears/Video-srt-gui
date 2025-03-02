import sys


from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


# 创建应用程序实例
app = QApplication(sys.argv)

# 创建主窗口实例
window = MainWindow()

# 显示窗口
window.show()

# 启动应用程序事件循环并返回退出代码
sys.exit(app.exec())

