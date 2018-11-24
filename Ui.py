from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.current_contact = None

    def __flash_init_Qt(self):
        #  from .ui import widgets
        #  self.InputBox.keyPressEvent = widgets.InputBox.keyPressEvent
        #  self.InputBox.keyPressEvent = QtWidgets.QTextEdit.keyPressEvent
        self.__init_FriendTree()
        self.__init_GroupTree()

    def __connect_event(self):
        """绑定的信号槽
        """
        self.__event_filter()
        self.FriendTree.doubleClicked.connect(
            self.__doubleclick_FriendTree_item)  # 双击联系人列表
        self.GroupTree.doubleClicked.connect(
            self.__doubleclick_GroupTree_item)  # 双击群组列表
        self.SendButton.clicked.connect(self.__send_message)  # 调取发送函数
        self.return_text_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return), self)
        self.return_text_shortcut.activated.connect(
            self.__add_return_to_InputBox)
        self.return_text_shortcut.setEnabled(False)
        # CTRL+回车 在Input Box添加回车

    def __add_return_to_InputBox(self):
        """在光标后添加一个回车
        """
        cursor = self.InputBox.textCursor()
        cursor.insertText('\n')
        cursor.movePosition(QtGui.QTextCursor.NextWord,
                            QtGui.QTextCursor.KeepAnchor)

    def __event_filter(self):
        """绑定事件过滤器
        """
        self.InputBox.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.InputBox:
            if QtWidgets.QApplication.focusWidget() == self.InputBox:
                self.return_text_shortcut.setEnabled(True)
            else:
                self.return_text_shortcut.setEnabled(False)
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Return:
                    self.InputBox.setText(
                        self.InputBox.toPlainText().rstrip('\n'))
                    self.SendButton.animateClick()
        else:
            self.return_text_shortcut.setEnabled(False)
        return super(MainPage, self).eventFilter(obj, event)

    def __init_FriendTree(self):
        friend_list = self.ChatObject.ChatList.FriendListObject()
        friend_info_list = friend_list.info.info()  # 好友信息
        if friend_info_list:
            self.FriendTree.clear()  # 清空联系人列表
            for i in friend_info_list:
                tree_widget = self.FriendTree
                self.load_contact_tree(tree_widget, i['category'], i)

    def __init_GroupTree(self):
        group_list = self.ChatObject.ChatList.GroupListObject()
        group_info_list = group_list.info.info()  # 群组信息
        if group_info_list:
            self.GroupTree.clear()  # 清空群组列表
            for i in group_info_list:
                tree_widget = self.GroupTree
                self.load_contact_tree(tree_widget, None, i)

    def __auto_refresh_ui(self):
        """定时刷新数据
        """
        self.refresh_MessageList_timer = QtCore.QTimer(self)
        self.refresh_MessageList_timer.timeout.connect(self.__load_MessageList)
        self.refresh_MessageList_timer.start(100)

    def __load_MessageList(self):
        """载入消息列表
        """

        def format_chat_record(chat_record_dict):
            """格式化消息信息
            """
            import time
            sender_name = chat_record_dict['sender_name']
            message_unit_time = chat_record_dict['message_unit_time']
            message_content = chat_record_dict['message_content']
            message_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(message_unit_time))
            message = message_time + '|' + \
                "{:<{x}}".format(sender_name, x=20) + message_content
            return message

        current_contact = self.current_contact
        if current_contact is None:
            return False
        chat_record = current_contact.get_chat_record()
        root = self.MessageList
        root_count = root.count()
        for i in range(root_count, len(chat_record)):
            message_content = format_chat_record(chat_record[i])
            new_message = QtWidgets.QListWidgetItem()
            new_message.setText(message_content)
            self.MessageList.addItem(new_message)
            self.MessageList.scrollToBottom()

    def __doubleclick_FriendTree_item(self):
        tree_widget = self.FriendTree
        self.__get_new_current_contact(tree_widget)

    def __doubleclick_GroupTree_item(self):
        tree_widget = self.GroupTree
        self.__get_new_current_contact(tree_widget)

    def __get_new_current_contact(self, tree_widget):
        ChatObject = self.ChatObject
        try:
            current_contact_id = int(str(tree_widget.currentItem()))  # 获取好友ID
            if tree_widget == self.FriendTree:
                self.current_contact = ChatObject.ChatIndividual.FriendObject(
                    current_contact_id)
            elif tree_widget == self.GroupTree:
                self.current_contact = ChatObject.ChatIndividual.GroupObject(
                    current_contact_id)
            self.MessageList.clear()
        except ValueError:
            pass
        else:
            self.InputBox.setFocus()  # 文本框获得焦点

    def __send_message(self):
        send_text = self.InputBox.toPlainText()
        self.InputBox.clear()
        # 发送键按下后获取输入框文本并清空
        if not len(send_text):
            return False
        current_contact = self.current_contact
        if current_contact:
            current_contact.message.send_message(send_text)

    def load_contact_tree(self, tree_widget, category, contact_info_list):
        from .ui.widgets import ChatTreeWidgetItem
        try:
            contact_markname = contact_info_list['markname']
        except KeyError:
            contact_markname = None
        if not contact_markname:
            contact_markname = contact_info_list['name']
        root = tree_widget.invisibleRootItem()
        root_count = root.childCount()
        root_category_text_list = [
            root.child(i).text(0) for i in range(root_count)
        ]
        contact_item = ChatTreeWidgetItem({
            'name': contact_markname,
            'id': contact_info_list['id']
        })
        contact_item.setFlags(QtCore.Qt.ItemIsSelectable
                              | QtCore.Qt.ItemIsUserCheckable
                              | QtCore.Qt.ItemIsEnabled)
        # 创建好友组件
        if category in root_category_text_list:
            category_widget = self.FriendTree.findItems(
                category, QtCore.Qt.MatchFixedString)[0]
        else:
            category_widget = ChatTreeWidgetItem({
                'name': category,
                'id': None
            })
            tree_widget.addTopLevelItem(category_widget)
            category_widget.setFlags(QtCore.Qt.ItemIsSelectable
                                     | QtCore.Qt.ItemIsDragEnabled
                                     | QtCore.Qt.ItemIsUserCheckable
                                     | QtCore.Qt.ItemIsEnabled)
        category_widget.addChild(contact_item)
        # 添加好友组件


def main(data):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainPage(data)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(None)
