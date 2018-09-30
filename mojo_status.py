class MojoLogFile():
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


class MojoStatus():
    def __init__(self, statusListWidget, post_data_list):
        from handlePostData import QrCode
        mojo_log_file = 'nohup.out'
        self.Qrcode = QrCode(post_data_list)
        self.post_data_list = post_data_list
        self.mojoLogFile = mojoLogFile(mojo_log_file)
        self.ListWidget = statusListWidget

    def readlines(mojo_log_file):
        mojo_log_list = self.mojoLog.readlines()
