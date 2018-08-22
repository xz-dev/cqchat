import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer
import os
import shutil
import time
import json
import threading
import datetime


class ShowImage(QWidget):
    def __init__(self, imagePath):
        super().__init__()
        self.imagePath = imagePath
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.autoClose)
        self.timer.start(100)
        self.title = 'PyQt5 image - pythonspot.com'
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
        pixmap = QPixmap(self.imagePath)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()

    def autoClose(self):
        if not os.path.exists(self.imagePath):
            self.close()


def showQrcode(path):
    app = QApplication(sys.argv)
    ex = ShowImage(path)
    sys.exit(app.exec_())


def scanFolder(start_time, path):
    file_list = os.listdir(path)
    useful_file_list = list()
    for tmp_file in file_list:
        tmp_time = datetime.datetime.strptime(tmp_file, '%Y-%m-%d %H:%M:%S.%f')
        if tmp_time >= start_time:
            tmp_file = path + tmp_file
            useful_file_list.append(tmp_file)
        else:
            time.sleep(0.2)
    return useful_file_list


def isStart(path, start_time):
    while True:
        while not os.path.exists(path):
            time.sleep(0.5)
        file_list = os.listdir(path)
        if len(file_list):
            useful_file_list = scanFolder(start_time, path)
            for tmp_file in useful_file_list:
                with open(tmp_file, 'r') as f:
                    load_dict = json.load(f)
                    if load_dict['event'] == 'input_qrcode':
                        qrcode_path = load_dict['params'][0]  # 获得二维码
            #  useful_file_list = scanFolder(start_time, path)
            #  for tmp_file in useful_file_list:
            #      with open(tmp_file, 'r') as f:
            #          load_dict = json.load(f)
            #          if load_dict['event'] == 'state_change' and load_dict['params'] == ['loading', 'scaning']:
                        if os.path.exists(qrcode_path):
                            show_qrcode = threading.Thread(
                                target=showQrcode, args=(qrcode_path,))
                            show_qrcode.start()
                            show_qrcode.join()
                            return True


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
        send_message_dict = handleFriendMessage(send_message_dict, path, bak_path)
        print(send_message_dict)
        time.sleep(5)
        #  print(message_dict)
        #  send_message_dict.send(message_dict)


if __name__ == '__main__':
    isStart('/tmp/pyqtWebQQ/')
