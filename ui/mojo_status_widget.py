class MojoStatusWidget():
    def refreshMojoStatusWidget(self):
        from PyQt5 import QtWidgets
        from PyQt5.QtCore import QSize
        mojo_log_list = self.mojoLogFile.readlines()
        if mojo_log_list:
            for mojo_log in mojo_log_list:
                newItem = QtWidgets.QListWidgetItem()
                newItem.setText(mojo_log)
                self.ListWidget.addItem(newItem)
        qrcode_imageItem = self.Qrcode.qrcodeListItem()
        if qrcode_imageItem:
            self.ListWidget.setIconSize(QSize(200, 200))
            self.ListWidget.addItem(qrcode_imageItem)
        self.ListWidget.scrollToBottom()
        return self.ListWidget
