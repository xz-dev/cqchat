from .info import Info
from .message import Message

__all__ = ['BaseContactObject', 'BaseChatListObject']


class BaseChatObject():
    def __init__(self):
        self.__call_children()
        self.info = lambda: list(Info(self.chat_object_id,
                                      self.chat_object_type))

    def __call_children(self):
        self.chat_object_id = getattr(self, 'chat_object_id')
        self.chat_object_type = getattr(self, 'chat_object_type')


class BaseContactObject(BaseChatObject):
    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.message = Message(self.chat_object_id, self.chat_object_type)

    def get_chat_record(self):
        all_chat_record = self.__data.chat_record
        chat_object_id = self.chat_object_id
        if chat_object_id not in all_chat_record:
            all_chat_record[chat_object_id] = list()
        chat_record = all_chat_record[chat_object_id]
        return chat_record


class BaseChatListObject(BaseChatObject):
    def __init__(self):
        super().__init__()
