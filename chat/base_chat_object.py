from .info import Info
from .message import Message

__all__ = ['BaseContactObject', 'BaseChatListObject']


class BaseChatObject():
    def __init__(self):
        self.__call_children()
        self.info = Info(self.chat_object_id, self.chat_object_type)

    def __call_children(self):
        self.chat_object_id = getattr(self, 'chat_object_id')
        self.chat_object_type = getattr(self, 'chat_object_type')
        #  self.chat_info_data = getattr(self, 'chat_info_data')

    #  def search_chat_info(self, match_dict):
    #      self.chat_info_data.search(match_dict)


class BaseContactObject(BaseChatObject):
    def __init__(self, data):
        self.__data = data
        super().__init__()
        self.message = Message(self.chat_object_id, self.chat_object_type)
        chat_record = self.__data.chat_record
        chat_object_id = self.chat_object_id
        if chat_object_id not in chat_record:
            chat_record[chat_object_id] = list()
        self.chat_record = chat_record[chat_object_id]


class BaseChatListObject(BaseChatObject):
    def __init__(self):
        super().__init__()
