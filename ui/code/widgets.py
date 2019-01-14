from PyQt5 import QtCore, QtWidgets

__all__ = [
    'ChatTreeWidgetItem',
    'InputBox',
]


class ChatTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, chat_info_dict):
        self.chat_info_dict = chat_info_dict
        super().__init__()
        object_name = chat_info_dict['name']
        _translate = QtCore.QCoreApplication.translate
        self.setText(0, _translate("MainWindow", object_name))

    def __str__(self):
        return str(self.chat_info_dict['id'])


class InputBox(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, qKeyEvent):
        print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            print('Enter pressed')
        else:
            super().keyPressEvent(qKeyEvent)
