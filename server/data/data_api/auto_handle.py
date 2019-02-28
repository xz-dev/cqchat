import multiprocessing as mp
import time

__all__ = [
    'HandlePostData',
]


class HandlePostData():
    def __init__(self, data):
        self.__data = data

    def run(self):
        try:
            while True:
                self.__sort_post_data()
        except KeyboardInterrupt:
            pass

    def __sort_post_data(self):
        """提取所有有关好友的消息
            (包括接收与发送)
            并整合为dict
            friend_message_dict[chat_object_id] = [{
                'message_id': message_id,
                'message_unit_time': message_unit_time,
                'message_content': message,
                'sender_name': sender_name,
                'sender_id': sender_id,
                'group_id': group_id,
                }, ...]
        """
        post_data = self.__data.post_data
        if len(post_data):
            message_dict_list = list()
            with mp.Pool() as pool:
                message_dict_list = pool.map(self._find_message,
                                             range(len(post_data)))
            message_dict_list = [i for i in message_dict_list if i]
            if len(message_dict_list):
                for single_message_list in message_dict_list:
                    self.__add_chat_record(single_message_list)
            else:
                time.sleep(0.2)
        else:
            time.sleep(0.2)

    def __add_chat_record(self, single_message_list):
        message_data = single_message_list[1]
        chat_record = self.__data.chat_record
        post_data = self.__data.post_data
        try:
            contact_object_id = message_data['contact_object_id']
            if contact_object_id in chat_record and chat_record[
                    contact_object_id]:
                tmp_list = chat_record[contact_object_id]
                # 确保列表顺序按时间顺序
                last_message_unit_time = tmp_list[-1]['message_unit_time']
                message_unit_time = message_data['message_unit_time']
                if last_message_unit_time <= message_unit_time:
                    tmp_list.append(message_data)
                else:
                    tmp_list.insert(-1, message_data)
                chat_record[contact_object_id] = tmp_list
            else:
                chat_record[contact_object_id] = [
                    message_data,
                ]
            numbering = single_message_list[0]
            del (post_data[numbering])
        except TypeError:
            pass

    def _find_message(self, numbering):
        """
        寻找消息并分类
        """
        post_json = self.__data.post_data[numbering]
        if post_json['post_type'] == 'message':
            message_id = post_json['message_id']
            sender_id = post_json['sender']['user_id']  # 发送者id
            if post_json['self_id'] == post_json['sender']['user_id']:
                sender_name = post_json['sender']['nickname'] + '(me)'
            else:
                sender_name = post_json['sender']['nickname']
            # 自我名字加后缀 (me)
            message_unit_time = post_json['time']
            message_content = post_json['raw_message']
            if post_json['message_type'] == 'private':
                # 好友聊天记录
                contact_object_type = post_json['user_id']
                contact_object_id = post_json['user_id']
            elif post_json['message_type'] == 'group':
                # 群组聊天记录
                contact_object_type = post_json['group_id']  # 群组id
                contact_object_id = post_json['group_id']
            single_message_dict = {
                'contact_object_type': contact_object_type,
                'contact_object_id': contact_object_id,
                'local_unix_time': post_json['local_unix_time'],  # 用于判断消息先后
                'message_id': message_id,
                'sender_id': sender_id,
                'sender_name': sender_name,
                'message_unit_time': message_unit_time,
                'message_content': message_content,
            }
        else:
            single_message_dict = None
        return numbering, single_message_dict

    def add_message_notification(self, single_message_dict):
        tray_message = self.tray_message
        tray_message.append(single_message_dict)
