from ..http import get, post

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
                self.__send_message_api = '/send_private_msg'
            elif self.__chat_object_type == 'group':
                self.__send_message_api = '/send_group_msg'
        return self.__send_message(str_message)

    def __send_message(self,
                       str_message,
                       is_https=0,
                       host='127.0.0.1',
                       port='5700'):
        api = self.__send_message_api
        chat_object_id = self.__chat_object_id
        if self.__chat_object_type == 'friend':
            payload = {'user_id': chat_object_id, 'message': str_message}
        elif self.__chat_object_type == 'group':
            payload = {'group_id': chat_object_id, 'message': str_message}
        try:
            resp_dict = get.get_api.get_data(payload=payload, api=api)
            if resp_dict['status'] == 'ok':
                self.__post_feedback(str_message,
                                     resp_dict['data']['message_id'])
                return True
            else:
                return False
        except Exception:
            return None

    def __post_feedback(self, str_message, message_id):
        import time
        get_data = get.get_api.get_data(payload=None, api='/get_login_info')
        porsonal_info = get_data['data']
        chat_object_id = self.__chat_object_id
        chat_object_type = self.__chat_object_type
        payload = {
            'font': None,
            'message': str_message,
            'message_id': message_id,
            'message_type': 'private',
            'post_type': 'message',
            'raw_message': str_message,
            'self_id': porsonal_info['user_id'],
            'sender': {
                'age': 0,
                'nickname': porsonal_info['nickname'],
                'sex': None,
                'user_id': porsonal_info['user_id'],
            },
            'sub_type': chat_object_type,
            'time': time.time(),
            'user_id': chat_object_id
        }
        resp = post.post_api.post_data(payload=payload)
        return resp
