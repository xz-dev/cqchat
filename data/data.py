import multiprocessing

__all__ = [
    'Data',
]


class BaseList():
    def __init__(self, manager):
        self.__data = manager.list()
        self.append = self.__data.append()

    def __repr__(self):
        return str(self.__data)

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return reversed(self.values)

    def __concat__(self, other):
        return self.__data + other

    def append(self, item):
        self.__data.append(item)


class BaseDict():
    def __init__(self, manager):
        self.__data = manager.dict()

    def __repr__(self):
        return str(self.__data)

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        tmp_dict = dict(self.__data)
        return iter(tmp_dict)

    def __delitem__(self, key):
        del (self.__data[key])

    def __bool__(self):
        if len(self.__data):
            return True
        else:
            return False

    def keys(self):
        return self.__data.keys()

    def clear(self):
        self.__data.clear()

    def add_list(self, key, value):
        data = self.__data
        if key in data:
            tmp_list = data[key]
            tmp_list.append(value)
            data[key] = tmp_list
        else:
            data[key] = [
                value,
            ]


class PostData(BaseDict):
    """Post信息字典
    """

    def __init__(self, manager):
        super().__init__(manager=manager)


class ChatRecord(BaseDict):
    """聊天记录字典
    chat_record['sender_id'] = [
            <first message dict>,
            <second message dict>,
            ...]
    """

    def __init__(self, manager):
        super().__init__(manager)


class GroupListDict(BaseDict):
    """群组列表字典
    """

    def __init__(self, manager):
        super().__init__(manager)


class FriendListDict(BaseDict):
    """好友列表字典
    """

    def __init__(self, manager):
        super().__init__(manager)


class TrayMessage(BaseList):
    """系统托盘消息提醒列表
    """

    def __init__(self, manager):
        super().__init__(manager)


class RunStatus(BaseDict):
    """程序运行状态字典
    """

    def __init__(self, manager):
        super().__init__(manager)


class UiData(BaseDict):
    """UI数据字典
    """

    def __init__(self, manager):
        super().__init__(manager)
        #  self.widget = UiWidget(manager)
        self.tmp_dict = BaseDict(manager)


#  class UiWidget():
#      def __init__(self, manager):
#          self.friend_tree = BaseDict(manager)
#          self.group_tree = BaseDict(manager)


class Data():
    """管理所有数据类
    """

    def __init__(self):
        manager = multiprocessing.Manager()  # 初始化manager
        self.chat_record = ChatRecord(manager)  # 聊天记录类
        self.post_data = PostData(manager)  # post信息类
        self.ui_data = UiData(manager)  # Ui数据 TODO: 暂作为空类, 待UI完成后完善
        self.status = RunStatus(manager)  # 运行状态
