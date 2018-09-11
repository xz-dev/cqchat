class mojoLogFile():
    def __init__(self, log_file):
        self.log_file = log_file

    def readlines(self):
        """
        读取mojo log文件
        """
        log_file = self.log_file
        mojo_log_list = list()
        try:
            with open(log_file, 'r') as f:
                mojo_log_list = f.readlines()
            open(log_file, 'w').close()
        finally:
            return mojo_log_list


class mojoStatus():
    def __init__(self, statusListWidget, post_data_list):
        from handlePostData import QrCode
        mojo_log_file='nohup.out'
        self.Qrcode = QrCode(post_data_list)
        self.post_data_list = post_data_list
        self.mojoLogFile = mojoLogFile(mojo_log_file)
        self.ListWidget = statusListWidget

    def readlines(mojo_log_file):
        mojo_log_list = self.mojoLog.readlines()
    def refreshMojoStatusWidget(self):
        from PyQt5 import QtWidgets
        from PyQt5.QtCore import QSize
        mojo_log_list = self.mojoLogFile.readlines()
        if mojo_log_list:
            for mojo_log in mojo_log_list:
                newItem = QtWidgets.QListWidgetItem()
                newItem.setText(mojo_log)
                self.ListWidget.addItem(newItem)
                self.ListWidget.scrollToBottom()
        #  post_data_list = self.post_data_list
        #  showQrcode = self.qrcodeQListWidget
        qrcode_imageItem = self.Qrcode.qrcodeListItem()
        if qrcode_imageItem:
            self.ListWidget.setIconSize(QSize(200, 200))
            self.ListWidget.addItem(qrcode_imageItem)
            self.ListWidget.scrollToBottom()
        return self.ListWidget
