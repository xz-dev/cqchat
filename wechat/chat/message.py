from ..data.get import get_api

__all__ = [
    'Message',
]


class Message():
    def __init__(self, chat_object_id, chat_object_type):
        self.__chat_object_id = chat_object_id
        self.__chat_object_type = chat_object_type
        self.__send_message_api = ''
        self.message_list = list()

    def send_message(self, str_message):
        if not self.__send_message_api:
            if self.__chat_object_type == 'friend':
                self.__send_message_api = '/openwx/send_friend_message'
            elif self.__chat_object_type == 'group':
                self.__send_message_api = '/openwx/send_group_message'
        return self.__send_message(str_message)

    def __send_message(self,
                       str_message,
                       is_https=0,
                       host='127.0.0.1',
                       port='3000'):
        api = self.__send_message_api
        chat_object_id = self.__chat_object_id
        payload = {'id': chat_object_id, 'content': str_message}
        try:
            resp_dict = get_api.get_data(payload=payload, api=api)
            if not resp_dict['code']:
                return True
            else:
                return False
        except Exception:
            return None
