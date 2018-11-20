import multiprocessing

__all__ = ['Data', ]


def search_dict(target_dict, match_dict):
    # 根据match_dict匹配target_dict
    try:
        numering = search_dict.key()
        search_dict = search_dict.value()
        if search_dict[term] == content:
            return numbering, search_dict
        else:
            return None
    except:
        return None


class BaseList():
    def __init__(self, message):
        self.data = manager.list()

    def add(self, item):
        self.data.append(item)


class BaseDict():
    def __init__(self, manager):
        self.data = manager.dict()

    def search(self, match_dict):
        with multiprocessing.Pool as pool:
            res = pool.map(
                partial(search_dict, match_dict=match_dict), self.data)
        res = [i for i in res if i is not None]
        return res

    def add(self, key, value):
        data = self.data
        if key in data:
            tmp_list = data[key]
            tmp_list.append(value)
            data[key] = tmp_list
        else:
            data[key] = [value, ]

    def replace(self, key, value):
        data = self.data
        data[key] = value

    def clear(self):
        self.data.clear()


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
        super().__init__(manager=manager)


class GroupListDict(BaseDict):
    """群组列表字典
    """

    def __init__(self, manager):
        super().__init__(manager=manager)


class FriendListDict(BaseDict):
    """好友列表字典
    """

    def __init__(self, manager):
        super().__init__(manager=manager)


class TrayMessage(BaseList):
    """系统托盘消息提醒列表
    """

    def __init__(self, manager):
        super().__init__(manager=manager)


class RunStatus(BaseDict):
    """程序运行状态字典
    """

    def __init__(self, manager):
        super().__init__(manager=manager)


class UiData(BaseDict):
    """UI数据字典
    """

    def __init__(self, manager):
        super().__init__(manager=manager)
        self.widget = UiWidget(manager)
        self.tmp_dict = BaseDict(manager)


class UiWidget():
    def __init__(self, manager):
        self.friend_tree = BaseDict(manager)
        self.group_tree = BaseDict(manager)


class Data():
    """管理所有数据类
    """

    def __init__(self):
        manager = multiprocessing.Manager()  # 初始化manager
        self.chat_record = ChatRecord(manager)  # 聊天记录类
        self.post_data = PostData(manager)  # post信息类
        self.ui_data = UiData(manager)  # Ui数据 TODO: 暂作为空类, 待UI完成后完善
        self.status = RunStatus(manager)  # 运行状态
