from .base_chat_object import *

__all__ = ['ChatObject', ]
#  __all__ = ['FriendObject', 'GroutObject',
#             'FriendListObject', 'GroupListObject']


class ChatObject():
    """聊天对象的初始类
    作用: 导入data数据
    """
    # TODO: 简化/删除此类

    def __init__(self, data):
        self.ChatList = ChatList()
        self.ChatIndividual = ChatIndividual(data)


class ChatList():
    # 所有列表类
    def FriendListObject(self):
        return FriendListObject()

    def GroupListObject(self):
        return GroupListObject()


class ChatIndividual():
    # 个体聊天对象
    def __init__(self, data):
        self.__data = data

    def FriendObject(self, chat_object_id):
        return FriendObject(self.__data, chat_object_id)

    def GroutObject(self, chat_object_id):
        return GroutObject(self.__data, chat_object_id)


class FriendListObject(BaseChatListObject):
    """好友列表
    """

    def __init__(self):
        self.chat_object_id = None
        self.chat_object_type = 'friend_list'
        super().__init__()


class GroupListObject(BaseChatListObject):
    """群组列表
    """

    def __init__(self):
        self.chat_object_id = None
        self.chat_object_type = 'group_list'
        super().__init__()


class FriendObject(BaseContactObject):
    """好友对象
    """

    def __init__(self, data, chat_object_id):
        self.chat_object_id = chat_object_id
        self.chat_object_type = 'friend'
        super().__init__(data)


class GroutObject(BaseContactObject):
    """群组对象
    """

    def __init__(self, data, chat_object_id):
        self.chat_object_id = chat_object_id
        self.chat_object_type = 'group'
        super().__init__(data)
