import multiprocessing as mp
import os
import time
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon


class QrCode():
    """
    显示二维码
    制作QListWidget
    """

    def __init__(self, post_data_list):
        self.post_data_list = post_data_list
        self.tmp_image_list = list()
        self.qrcode_base64_str = str()

    def qrcodeListItem(self):
        post_data_list = self.post_data_list
        qrcode_imageItem = None
        if post_data_list:
            res = []
            pool = mp.Pool()
            findBase64Qrcode = self.findBase64Qrcode
            res = pool.map(findBase64Qrcode, post_data_list)
            pool.close()
            pool.join()
            res = [i for i in res if type(i) is str]
            qrcode_base64_str = self.qrcode_base64_str
            if res:
                post_data_list[:] = []
                self.qrcode_base64_str = res[0]
                tmp_image_list = self.base64ToImage()
                self.tmp_image_list = tmp_image_list
                qrcode_imageItem = self.makeQrcodeListItem()
        return qrcode_imageItem

    def findBase64Qrcode(self, post_json):
        """
        查询QrCode的base64编码
        """
        if post_json['post_type'] == 'event':
            if post_json['event'] == 'input_qrcode':
                qrcode_base64 = post_json['params'][1]
                return qrcode_base64
            elif post_json['params'] == ['updating', 'running']:
                return True
            else:
                return False
        else:
            return False

    def base64ToImage(self):
        """
        base64转图片
        """
        import base64
        import tempfile
        base64_str = self.qrcode_base64_str
        base64_byte = base64_str.encode()
        tmp_image = tempfile.mkstemp(suffix='.png')
        tmp_image_name = tmp_image[1]
        with open(tmp_image_name, 'wb') as img:
            img.write(base64.decodebytes(base64_byte))
        return tmp_image

    def makeQrcodeListItem(self):
        """
        创建QrCode QListWidgetItem
        """
        qrcode_image = self.tmp_image_list[1]
        newItem = QtWidgets.QListWidgetItem()
        newItem.setIcon(QIcon(qrcode_image))
        os.remove(qrcode_image)
        return newItem


def handleMessageContent(message_unit_time, sender_name, message_content):
    """
    格式化消息信息
    """
    if message_unit_time and sender_name and message_content:
        message_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(message_unit_time))
        message = message_time + '|' + \
            "{:<{x}}".format(sender_name, x=20) + message_content
    else:
        message = None
    return message


def findMessage(post_json):
    """
    寻找消息并分类
    """
    if post_json['post_type'] != 'event':
        message_id = None
        sender_id = None
        sender_name = None
        message_unit_time = None
        message_content = None
        if post_json['post_type'] == 'receive_message' and post_json['class'] == 'recv':
            # 接收消息
            if post_json['type'] == 'friend_message':
                # 获取好友发送的消息
                message_id = post_json['id']
                group_name = None
                group_id = None
                sender_id = post_json['sender_id']  # 发送id 即好友id
                sender_name = post_json['sender']
                message_unit_time = post_json['time']
                message_content = post_json['content']
            elif post_json['type'] == 'group_message':
                # 获取群组发送的消息
                message_id = post_json['id']
                group_name = post_json['group']
                group_id = post_json['group_id']  # 群组id
                sender_id = post_json['sender_id']  # 发言群员id
                sender_name = post_json['sender']
                message_unit_time = post_json['time']
                message_content = post_json['content']
        elif post_json['post_type'] == 'send_message' and post_json['class'] == 'send':
            if post_json['type'] == 'friend_message':
                # 自己发给好友的消息
                message_id = post_json['id']
                group_name = None
                group_id = None
                sender_name = post_json['sender'] + "(me)"
                sender_id = post_json['receiver_id']  # 隐藏自己的id, 替换为好友id
                message_unit_time = post_json['time']
                message_content = post_json['content']
            elif post_json['type'] == 'group_message':
                # 自己发给群组的消息
                message_id = post_json['id']
                group_name = post_json['group']
                group_id = post_json['group_id']  # 群组id
                sender_id = post_json['sender_id']
                sender_name = post_json['sender'] + "(me)"
                message_unit_time = post_json['time']
                message_content = post_json['content']
        message = handleMessageContent(message_unit_time=message_unit_time,
                                       sender_name=sender_name,
                                       message_content=message_content)
        single_message_dict = {'message_id': message_id,
                               # 用于判断消息先后
                               'local_unix_time': post_json['local_unix_time'],
                               'message_unit_time': message_unit_time,
                               'message_content': message,
                               'sender_name': sender_name,
                               'sender_id': sender_id,
                               'group_name': group_name,
                               'group_id': group_id,
                               }

    else:
        single_message_dict = None
    return single_message_dict


def addMessageNotification(single_message_dict, all_message_dict):
    if 'message_notification_list' in all_message_dict:
        message_notification_list = all_message_dict['message_notification_list']
        for tmp_list in message_notification_list:
            message_dict_last_message_unit_time = tmp_list[-1]['message_unit_time']
            message_unit_time = single_message_dict['message_unit_time']
            if message_dict_last_message_unit_time <= message_unit_time:
                message_notification_list.append(single_message_dict)
            else:
                message_notification_list.insert(-1, single_message_dict)
        all_message_dict['message_notification_list'] = message_notification_list
    else:
        all_message_dict['message_notification_list'] = [single_message_dict, ]


def removeRecordedManssage(message_id, post_data_list):
    """
    从POST数据中移除已处理消息
    """
    for post_json in post_data_list:
        if 'id' in post_json and post_json['id'] == message_id:
            post_data_list.remove(post_json)


def getMessage(post_data_list, all_message_dict):
    """
    提取所有有关好友的消息
    (包括接收与发送)
    并整合为dict
    friend_message_dict[chat_object_id] = [{
        'message_id': message_id,
        'message_unit_time': message_unit_time,
        'message_content': message,
        'sender_name': sender_name,
        'sender_id': sender_id,
        'group_name': group_name,
        'group_id': group_id,
        }, ...]
    """
    pool = mp.Pool()
    while post_data_list != False:
        if len(post_data_list):
            message_dict_list = pool.map(findMessage, post_data_list)
            message_dict_list = [i for i in message_dict_list if i != None]
            if len(message_dict_list):
                for single_message_dict in message_dict_list:
                    removeRecordedManssage(single_message_dict['message_id'],
                                           post_data_list)
                    addMessageNotification(single_message_dict,
                                           all_message_dict)
                    if single_message_dict['group_id']:
                        sender_id = single_message_dict['group_id']
                    else:
                        sender_id = single_message_dict['sender_id']
                    if sender_id in all_message_dict:
                        tmp_list = all_message_dict[sender_id]
                        # 确保列表顺序按时间顺序
                        message_dict_last_message_unit_time = tmp_list[-1]['message_unit_time']
                        message_unit_time = single_message_dict['message_unit_time']
                        if message_dict_last_message_unit_time <= message_unit_time:
                            tmp_list.append(single_message_dict)
                        else:
                            tmp_list.insert(-1, single_message_dict)
                        all_message_dict[sender_id] = tmp_list
                    else:
                        tmp_list = [single_message_dict]
                        all_message_dict[sender_id] = tmp_list
            else:
                time.sleep(0.2)
        else:
            time.sleep(0.2)
#  def run(post_data_list, all_message_dict):
#
