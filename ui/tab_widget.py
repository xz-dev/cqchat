from PyQt5 import QtWidgets

__all__ = ['ChatTabWidget', ]


class BaseInfoTabItem(QtWidgets.QWidget):
    def __init__(self, object_name):
        super().__init__()
        self.setObjectName(object_name)


class InfoTabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setTabBarAutoHide(False)
        verticalLayout = QtWidgets.QVBoxLayout(BaseInfoTabItem)
    def
