from ..data.get import get_api

__all__ = ['Info', ]


class Info():
    def __init__(self, chat_object_id, chat_object_type):
        self.__chat_object_id = chat_object_id
        self.__chat_object_type = chat_object_type
        self.__info_api = ''
        self.__info_data = None

    def __iter__(self):
        if not self.__info_data:
            self.reflash_info_data()
        return iter(self.__info_data)

    def __get_info(self, is_https=0, host='127.0.0.1', port='3000'):
        api = self.__info_api
        chat_object_id = self.__chat_object_id
        payload = {'id': chat_object_id, }
        try:
            resp = get_api.get_data(payload=payload, api=api)
            resp_dict = resp[0]
            return resp_dict
        except KeyError:
            return None

    def __get_list_info(self, is_https=0, host='127.0.0.1', port='3000'):
        api = self.__info_api
        payload = None
        print(get_api.get_data(payload=payload, api=api))
        return get_api.get_data(payload=payload, api=api)

    def reflash_info_data(self):
        chat_object_type = self.__chat_object_type
        if not self.__info_api:
            if 'list' in chat_object_type:
                if chat_object_type == 'friend_list':
                    self.__info_api = '/openwx/get_friend_info'
                elif chat_object_type == 'group_list':
                    self.__info_api = '/openwx/get_group_info'
                self.__info_data = self.__get_list_info()
            else:
                if chat_object_type == 'friend':
                    self.__info_api = '/openwx/search_friend'
                elif chat_object_type == 'group':
                    self.__info_api = '/openwx/search_group'
                self.__info_data = self.__get_info()
