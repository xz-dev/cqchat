import multiprocessing as mp
import time

__all__ = ['PostData', ]


class HandlePostData():
    def __init__(self):
        pass

    def run(self, Data):
        try:
            self.__data = Data
            while True:
                s = self.__data.chat_record.data
                self.__sort_post_data()
                #  if s != self.__data.chat_record.data:
                #      print("=========")
                #      print(self.__data.chat_record.data)
        except KeyboardInterrupt:
            pass

    def __sort_post_data(self):
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
        post_data = self.__data.post_data
        if len(post_data.data):
            message_dict_list = list()
            with mp.Pool() as pool:
                message_dict_list = pool.map(
                    self._find_message, range(len(post_data.data)))
            message_dict_list = [i for i in message_dict_list if i != None]
            if len(message_dict_list):
                for single_message_list in message_dict_list:
                    numbering = single_message_list[0]
                    message_data = single_message_list[1]
                    self.__add_chat_record(message_data)
            else:
                time.sleep(0.2)
        else:
            time.sleep(0.2)

    def __add_chat_record(self, message_data):
        chat_record = self.__data.chat_record.data
        try:
            if message_data['group_id']:
                sender_id = message_data['group_id']
            else:
                sender_id = message_data['sender_id']
            if sender_id in chat_record:
                tmp_list = chat_record[sender_id]
                # 确保列表顺序按时间顺序
                last_message_unit_time = tmp_list[-1]['message_unit_time']
                message_unit_time = message_data['message_unit_time']
                if last_message_unit_time <= message_unit_time:
                    tmp_list.append(message_data)
                else:
                    tmp_list.insert(-1, message_data)
                chat_record[sender_id] =  tmp_list
            else:
                chat_record[sender_id] = [message_data, ]
            del(post_data.data[numbering])
        except TypeError:
            pass

    def _find_message(self, numbering):
        """
        寻找消息并分类
        """
        post_json = self.__data.post_data.data[numbering]
        #  print(post_json)
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
            single_message_dict = {'message_id': message_id,
                                   # 用于判断消息先后
                                   'local_unix_time': post_json['local_unix_time'],
                                   'message_unit_time': message_unit_time,
                                   'message_content': message_content,
                                   'sender_name': sender_name,
                                   'sender_id': sender_id,
                                   'group_name': group_name,
                                   'group_id': group_id,
                                   }

        else:
            single_message_dict = None
        return numbering, single_message_dict

    def add_message_notification(self, single_message_dict):
        tray_message = self.tray_message
        tray_message.append(single_message_dict)

    #  def remove_manssage(self, message_id, post_data_list):
    #      """
    #      从POST数据中移除特定消息
    #      """
    #      for post_json in post_data_list:
    #          if 'id' in post_json and post_json['id'] == message_id:
    #              post_data_list.remove(post_json)

    def handle_message_content(message_unit_time, sender_name, message_content):
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
