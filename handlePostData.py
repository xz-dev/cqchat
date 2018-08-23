import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer
import multiprocessing as mp
import os
import shutil
import time
import json
import threading
import datetime


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
    print(post_data_list)
    showQrcode(res[0])


def handleFriendMessage(message_dict, path, bak_path):
    """
    提取所有好友的消息
    并整合为dict
    {id:(receive_time, receive_content), ...}
    """
    if os.path.exists(path):
        file_list = os.listdir(path)
        if len(file_list):
            id_list = message_dict.keys()
            for tmp_file in file_list:
                receive_time = datetime.datetime.strptime(
                    tmp_file, '%Y-%m-%d %H:%M:%S.%f')
                tmp_file = path + tmp_file
                with open(tmp_file, 'r') as f:
                    load_dict = json.load(f)
                    # 添加新消息
                    if load_dict['post_type'] == 'receive_message' and load_dict['class'] == 'recv':
                        sender_name = load_dict['sender']
                        sender_id = load_dict['sender_id']
                        receive_content = load_dict['content']
                        message_list = (receive_time, receive_content)
                        if sender_id not in id_list:
                            message_dict[sender_id] = [message_list]
                        else:
                            message_dict[sender_id].append([message_list])
                        # 移动原文件至备份文件夹
                        # 没有备份文件夹则创建
                        if not os.path.exists(bak_path):
                            os.makedirs(bak_path)
                        sender_dir = bak_path + str(sender_id) + '/'
                        if not os.path.exists(sender_dir):
                            os.makedirs(sender_dir)
                        shutil.move(tmp_file, sender_dir+str(receive_time))
        else:
            time.sleep(0.2)
    else:
        time.sleep(0.2)
    return message_dict


def processGetFriendMessage(send_message_dict, path, bak_path):
    while True:
        send_message_dict = handleFriendMessage(
            send_message_dict, path, bak_path)
        print(send_message_dict)
        time.sleep(5)
        #  print(message_dict)
        #  send_message_dict.send(message_dict)


if __name__ == '__main__':
    isStart('/tmp/pyqtWebQQ/')
