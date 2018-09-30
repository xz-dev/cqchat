from .base_chat_object import *

__all__ = ['FriendObject', 'GroutObject',
           'FriendListObject', 'GroupListObject']


class FriendListObject(BaseChatListObject):
    def __init__(self):
        self.chat_object_id = None
        self.chat_object_type = 'friend_list'
        super().__init__()


class GroupListObject(BaseChatListObject):
    def __init__(self):
        self.chat_object_id = None
        self.chat_object_type = 'group_list'
        super().__init__()


class FriendObject(BaseContactObject):
    def __init__(self, chat_object_id):
        self.chat_object_id = chat_object_id
        self.chat_object_type = 'friend'
        super().__init__()


class GroutObject(BaseContactObject):
    def __init__(self, chat_object_id):
        self.chat_object_id = chat_object_id
        self.chat_object_type = 'group'
        super().__init__()
