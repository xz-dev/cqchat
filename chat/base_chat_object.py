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


class BaseContactObject(BaseChatObject):
    def __init__(self):
        super().__init__()
        self.message = Message(self.chat_object_id, self.chat_object_type)


class BaseChatListObject(BaseChatObject):
    def __init__(self):
        super().__init__()
