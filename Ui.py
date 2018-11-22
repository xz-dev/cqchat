from PyQt5 import QtWidgets, QtCore
from . import MainGui


class MainPage(QtWidgets.QMainWindow, MainGui.Ui_MainWindow):
    """显示主页面
    """

    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        # 显示UI
        self.__data = data
        self.__init_data()
        self.__flash_init_Qt()
        self.__connect_event()
        self.__auto_refresh_ui()

    def __init_data(self):
        from .chat.chat_object import ChatObject
        self.ChatObject = ChatObject(self.__data)
        # 初始化ChatObject, 避免重复初始化

    def __connect_event(self):
        """绑定的信号槽
        """
        self.FriendTree.doubleClicked.connect(
            self.__doubleclick_FriendTree_item)  # 调取发送函数

    def __flash_init_Qt(self):
        self.__init_friend_list()

    def __init_friend_list(self):
        friend_list = self.ChatObject.ChatList.FriendListObject()
        friend_info_list = friend_list.info.info()  # 好友信息
        if friend_info_list:
            #  self.__data.ui_data.widget.friend_tree.clear()
            self.FriendTree.clear()  # 清空联系人列表
            for i in friend_info_list:
                tree_widget = self.FriendTree
                self.load_contact_tree(tree_widget, i['category'], i)

    def __auto_refresh_ui(self):
        """定时刷新数据
        """
        self.refresh_MessageList_timer = QtCore.QTimer(self)
        self.refresh_MessageList_timer.timeout.connect(self.__load_MessageList)
        self.refresh_MessageList_timer.start(100)

    def __load_MessageList(self):
        """载入消息列表
        """
        ui_data = self.__data.ui_data
        if 'current_contact_id' in ui_data.tmp_dict.keys():
            current_contact = self.ChatObject.ChatIndividual.FriendObject(
                ui_data.tmp_dict['current_contact_id'])
        else:
            return False
        chat_record = current_contact.chat_record
        root = self.MessageList
        root_count = root.count()
        #  message_list = [
        #     chat_record[i] for i in range(root_count, len(chat_record))
        #  ]
        for i in range(root_count, len(chat_record)):
            message_content = chat_record[i]['message_content']
            new_message = QtWidgets.QListWidgetItem()
            new_message.setText(message_content)
            self.MessageList.addItem(new_message)
            self.MessageList.scrollToBottom()

    def __doubleclick_FriendTree_item(self):
        try:
            self.__data.ui_data.tmp_dict['current_contact_id'] = int(
                str(self.FriendTree.currentItem()))  # 获取好友ID
        except ValueError:
            pass
        else:
            self.InputBox.setFocus()  # 文本框获得焦点

    def load_contact_tree(self, tree_widget, category, friend_info_list):
        from .ui.widgets import ChatTreeWidgetItem
        try:
            friend_markname = friend_info_list['markname']
        except KeyError:
            friend_markname = None
        if not friend_markname:
            friend_markname = friend_info_list['name']
        #  root = self.FriendTree.invisibleRootItem()
        root = tree_widget.invisibleRootItem()
        root_count = root.childCount()
        root_category_text_list = [
            root.child(i).text(0) for i in range(root_count)
        ]
        friend_item = ChatTreeWidgetItem({
            'name': friend_markname,
            'id': friend_info_list['id']
        })
        friend_item.setFlags(QtCore.Qt.ItemIsSelectable
                             | QtCore.Qt.ItemIsUserCheckable
                             | QtCore.Qt.ItemIsEnabled)
        # 创建好友组件
        if category in root_category_text_list:
            category_widget = self.FriendTree.findItems(
                category, QtCore.Qt.MatchFixedString)[0]
        else:
            category_widget = QtWidgets.QTreeWidgetItem([category])
            self.FriendTree.addTopLevelItem(category_widget)
            category_widget.setFlags(QtCore.Qt.ItemIsSelectable
                                     | QtCore.Qt.ItemIsDragEnabled
                                     | QtCore.Qt.ItemIsUserCheckable
                                     | QtCore.Qt.ItemIsEnabled)
        category_widget.addChild(friend_item)
        # 添加好友组件


def main(data):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainPage(data)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(None)
