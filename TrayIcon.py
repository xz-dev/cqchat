from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5.QtGui import QIcon


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.showMenu()
        self.showIcon()
        self.connectEvent()

    def connectEvent(self):
        self.activated.connect(self.iconClied)
        # 把鼠标点击图标的信号和槽连接

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()

    def showMenu(self):
        self.menu = QMenu()
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

    def showIcon(self):
        self.setIcon(QIcon("./icon/tray_icon.png"))
        self.icon = self.MessageIcon()

    def quit(self):
        "保险起见，为了完整的退出"
        self.setVisible(False)
        self.parent().close()
        qApp.quit()
        sys.exit()


def showQrcode(image_path):
    app = QApplication(sys.argv)
    ex = ShowImage(image_path)
    sys.exit(app.exec_())
