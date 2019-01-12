from ..http import get

__all__ = ['Info', ]


class Info():
    def __init__(self, chat_object_id, chat_object_type):
        self.__chat_object_id = chat_object_id
        self.__chat_object_type = chat_object_type
        self.__info_api = ''
        self.__info_data = None

    def __get_info(self, is_https=0, host='127.0.0.1', port='5700'):
        api = self.__info_api
        chat_object_id = self.__chat_object_id
        payload = {
            'id': chat_object_id,
        }
        try:
            resp = get.get_api.get_data(payload=payload, api=api)
            resp_dict = resp[0]
            return resp_dict
        except Exception:
            return None

    def __get_list_info(self, is_https=0, host='127.0.0.1', port='5700'):
        api = self.__info_api
        payload = None
        return get.get_api.get_data(payload=payload, api=api)

    def reflash_info_data(self):
        chat_object_type = self.__chat_object_type
        if not self.__info_api:
            if 'list' in chat_object_type:
                if chat_object_type == 'friend_list':
                    self.__info_api = '/_get_friend_list'
                elif chat_object_type == 'group_list':
                    self.__info_api = '/get_group_list'
                self.__info_data = self.__get_list_info()
            else:
                if chat_object_type == 'friend':
                    #  self.__info_api = '/openqq/search_friend'
                    self.__info_data = list()
                elif chat_object_type == 'group':
                    #  self.__info_api = '/openqq/search_group'
                    self.__info_data = list()
                self.__info_data = self.__get_info()

    def info(self):
        if not self.__info_data:
            self.reflash_info_data()
        return self.__info_data
