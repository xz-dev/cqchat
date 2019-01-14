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
        from ...server.chat.chat_object import ChatObject
        self.ChatObject = ChatObject(self.__data)
        # 初始化ChatObject, 避免重复初始化
        self.current_contact = None

    def __flash_init_Qt(self):
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
                    self.InputBox.setText(self.InputBox.toPlainText())
                    self.SendButton.animateClick()
        else:
            self.return_text_shortcut.setEnabled(False)
        return super(MainPage, self).eventFilter(obj, event)

    def __init_FriendTree(self):
        friend_list_object = self.ChatObject.ChatList.FriendListObject()
        friend_group_list = friend_list_object.info.info()  # 好友信息
        if friend_group_list:
            self.FriendTree.clear()  # 清空联系人列表
            for friend_group in friend_group_list['data']:
                tree_widget = self.FriendTree
                for contack_info_dict in friend_group['friends']:
                    self.load_contact_tree(tree_widget,
                                           friend_group['friend_group_name'],
                                           contack_info_dict)

    def __init_GroupTree(self):
        group_list_object = self.ChatObject.ChatList.GroupListObject()
        group_list = group_list_object.info.info()  # 群组信息
        if group_list:
            self.GroupTree.clear()  # 清空群组列表
            for group in group_list['data']:
                tree_widget = self.GroupTree
                self.load_contact_tree(tree_widget, None, group)

    def __auto_refresh_ui(self):
        """定时刷新数据
        """
        self.refresh_MessageList_timer = QtCore.QTimer(self)
        self.refresh_MessageList_timer.timeout.connect(
            self.__switch_chat_object)
        self.refresh_MessageList_timer.start(50)

    def __switch_chat_object(self):
        # 切换聊天对象
        self.__load_MessageList()
        self.__rename_ChatTab()

    def __rename_ChatTab(self):
        ChatTabWidget = self.ChatTabWidget
        current_contact = self.current_contact
        try:
            ChatTabWidget.setTabText(ChatTabWidget.currentIndex(),
                                     str(current_contact.chat_object_name))
        except AttributeError:
            pass

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
        try:
            selected_contact_id = int(str(tree_widget.currentItem()))
        except ValueError:
            return False
        else:
            try:
                current_contact_id = self.current_contact.chat_object_id
            except AttributeError:
                pass
            else:
                if current_contact_id == selected_contact_id:
                    return False
            finally:
                current_contact_id = selected_contact_id
                ChatIndividual = self.ChatObject.ChatIndividual
                chat_object_info_dict = {
                    'name': tree_widget.currentItem().text(0),
                    'id': current_contact_id
                }
                if tree_widget is self.FriendTree:
                    self.current_contact = ChatIndividual.FriendObject(
                        chat_object_info_dict)
                elif tree_widget is self.GroupTree:
                    self.current_contact = ChatIndividual.GroupObject(
                        chat_object_info_dict)
                self.MessageList.clear()
                self.InputBox.setFocus()  # 文本框获得焦点
        return True

    def __send_message(self):
        send_text = self.InputBox.toPlainText()[1:]
        self.InputBox.clear()
        # 发送键按下后获取输入框文本并清空
        if not len(send_text):
            return False
        current_contact = self.current_contact
        if current_contact:
            current_contact.message.send_message(send_text)

    def load_contact_tree(self, tree_widget, category, contack_info_dict):
        contack_info_dict = rename_keys(contack_info_dict)
        from .widgets import ChatTreeWidgetItem
        category = str(category)
        try:
            contact_markname = contack_info_dict['remark']
        except KeyError:
            contact_markname = None
        if not contact_markname:
            contact_markname = contack_info_dict['name']
        root = tree_widget.invisibleRootItem()
        root_count = root.childCount()
        root_category_text_list = [
            root.child(i).text(0) for i in range(root_count)
        ]
        contact_item = ChatTreeWidgetItem({
            'name': contact_markname,
            'id': contack_info_dict['id']
        })
        contact_item.setFlags(QtCore.Qt.ItemIsSelectable
                              | QtCore.Qt.ItemIsUserCheckable
                              | QtCore.Qt.ItemIsEnabled)
        # 创建好友组件
        if category in root_category_text_list:
            category_widget = tree_widget.findItems(
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


def rename_keys(in_dict):
    out_dict = dict()
    try:
        out_dict['id'] = in_dict['user_id']
        out_dict['name'] = in_dict['nickname']
        out_dict['remark'] = in_dict['remark']
    except KeyError:
        out_dict['id'] = in_dict['group_id']
        out_dict['name'] = in_dict['group_name']
    return out_dict


if __name__ == '__main__':
    main(None)
