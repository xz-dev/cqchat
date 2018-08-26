import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer
import multiprocessing as mp
import os
import time


class ShowImage(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.autoClose)
        self.timer.start(100)
        self.title = 'QrCode'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        pixmap = QPixmap(self.image_path)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()

    def autoClose(self):
        if not os.path.exists(self.image_path):
            self.close()


def showQrcode(image_path):
    app = QApplication(sys.argv)
    ex = ShowImage(image_path)
    sys.exit(app.exec_())


def findQrcode(post_json):
    if post_json['event'] == 'input_qrcode':
        return post_json['params'][0]
    elif post_json['params'] == ['loading', 'scaning']:
        return True
    else:
        return False


def isStart(post_data_list):
    pool = mp.Pool()
    res = []
    while len(res) != 1:
        while not res.count(True):
            res = pool.map(findQrcode, post_data_list)
        res = [i for i in res if type(i) is str]
    post_data_list[:] = []
    showQrcode(res[0])
    return True


def findFriendMessage(post_json):
    if post_json['post_type'] == 'receive_message' and post_json['class'] == 'recv' and post_json['type'] == 'friend_message':
        # 获取好友发送的消息
        message_id = post_json['id']
        friend_id = post_json['sender_id']  # 发送id 即好友id
        sender_name = post_json['sender']
        message_time = post_json['time']
        message_content = post_json['content']
        single_message_list = (friend_id, (message_id, message_time, sender_name, message_content))
    elif post_json['post_type'] == 'send_message' and post_json['class'] == 'send' and post_json['type'] == 'friend_message':
        message_id = post_json['id']
        friend_id = post_json['receiver_id']  # 接收id 即好友id
        sender_name = post_json['sender'] + "(me)"
        message_time = post_json['time']
        message_content = post_json['content']
        single_message_list = (friend_id, (message_id, message_time, sender_name, message_content))
    else:
        single_message_list = False
    return single_message_list


def removeRecordedManssage(message_id, post_data_list):
    for post_json in post_data_list:
        if 'id' in post_json and post_json['id'] == message_id:
            post_data_list.remove(post_json)


def getFriendMessage(post_data_list, friend_message_dict):
    """
    提取所有有关好友的消息
    (包括接收与发送)
    并整合为dict
    {id:[(message_time, sender_name, message_content)], ...}
    """
    pool = mp.Pool()
    #  tmp_friend_message_dict = dict()
    while True:
        if len(post_data_list):
            message_list = pool.map(findFriendMessage, post_data_list)
            message_list = [i for i in message_list if i not in [False, None]]
            if len(message_list):
                for tmp_list in message_list:
                    sender_id = tmp_list[0]
                    message = tmp_list[1]
                    message_id = tmp_list[1][0]
                    removeRecordedManssage(message_id, post_data_list)
                    if sender_id in friend_message_dict.keys():
                        item = friend_message_dict[sender_id]
                        item.append(message)
                        friend_message_dict[sender_id] = item
                    else:
                        item = friend_message_dict[sender_id] = list()
                        item.append(message)
                        friend_message_dict[sender_id] = item
                # 因无法直接操作friend_message_dict
                # 采用以下解决方案
                # https://stackoverflow.com/questions/35202278/cannot-append-items-to-multiprocessing-shared-list
            else:
                time.sleep(0.2)
        else:
            time.sleep(0.2)


if __name__ == '__main__':
    isStart('/tmp/pyqtWebQQ/')
