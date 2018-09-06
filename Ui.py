import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget, QLabel
import MainGui
import TrayIcon

import sendMessage
import handlePostData
import handleMojoStatusLog
from get import getInfo
import searchInfo
from TrayIcon import TrayIcon


class MainPage(QtWidgets.QMainWindow, MainGui.Ui_MainWindow, QSystemTrayIcon):
    """
    显示主页面
    """

    def __init__(self, all_message_dict, post_data_list, parent=None):
        self.showQrcode = handlePostData.showQrcode(post_data_list)
        super(MainPage, self).__init__(parent)
        self.ti = TrayIcon(self)
        self.ti.show()
        # 系统托盘图标
        super().__init__()
        self.all_message_dict = all_message_dict
        self.post_data_list = post_data_list
        self.is_start = False
        self.is_stop = False
        self.status_dict = {
            'is_start': False,
            'is_stop': False,
        }
        # TODO: 监控POST以实时调整信息
        self.loaded_message_info_dict = dict()  # 已加载的消息列表
        self.friendTree_widget_dict = dict()  # 好友列表数据
        self.groupTree_widget_dict = dict()  # 群组列表数据
        self.chat_object_info_dict = {'id': None, 'chat_type': None}
        # 当前的聊天对象
        self.friend_info_dict_list = list()
        self.group_info_dict_list = list()
        # friend_info_list 与 group_info_list只做备份列表用于查看是否有更改
        self.search_contact_result_dict = dict()  # 搜索所有联系人结果字典
        self.setupUi(self)
        self.autoRefreshData()
        self.connectEvent()

    def connectEvent(self):
        """
        绑定的信号槽
        """
        self.sendButton.clicked.connect(self.sendMessage)  # 调取发送函数
        self.friendTree.clicked.connect(self.clickFriendTree)  # 获取选中的好友ID
        self.groupTree.clicked.connect(self.clickGroupTree)  # 获取选中的群组ID
        self.sendButton.setShortcut("Ctrl+Return")  # CTRL + 回车键绑定发送键
        self.searchContactBar.textEdited.connect(
            self.searchContactBarTextEdited)  # 启动搜索功能
        self.searchContactList.doubleClicked.connect(
            self.doubleClickedsearchContactList)
        self.contactTabWidget.currentChanged.connect(
            self.clickContactTabWidget)
        # 获取选中搜索目标的信息

    def autoRefreshData(self):
        """
        定时刷新数据
        """
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.loadFriendTree)  # 绘出好友列表
        self.timer2 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.loadGroupTree)  # 绘出群组列表
        self.timer3 = QtCore.QTimer(self)
        self.timer3.timeout.connect(self.loadMessageList)
        self.timer3.start(50)
        self.timer4 = QtCore.QTimer(self)
        self.timer4.timeout.connect(self.messageNotification)
        self.timer4.start(50)
        self.timer5 = QtCore.QTimer(self)
        self.timer5.timeout.connect(self.loadStatusTextEdit)
        self.timer5.start(100)

    def trayMenu(self):
        """
        系统托盘
        """
        self.quitAction = QAction("退出", self, triggered=self.quit)
        # 系统托盘退出菜单

    def loadStatusTextEdit(self):
        """
        加载mojo后端状态框
        """
        mojo_log_file = 'nohup.out'
        mojo_log_list = handleMojoStatusLog.readMojoLog(mojo_log_file)
        if mojo_log_list:
            for mojo_log in mojo_log_list:
                newItem = QtWidgets.QListWidgetItem()
                newItem.setText(mojo_log)
                self.statusListWidget.addItem(newItem)
                self.statusListWidget.scrollToBottom()
        post_data_list = self.post_data_list
        showQrcode = self.showQrcode
        qrcode_imageItem = showQrcode.getQrcode()
        if qrcode_imageItem:
            self.statusListWidget.setIconSize(QSize(200, 200))
            self.statusListWidget.addItem(qrcode_imageItem)
            self.statusListWidget.scrollToBottom()

    def clickContactTabWidget(self):
        """
        点击TAB栏切换界面
        """
        currentIndex = self.contactTabWidget.currentIndex()
        if currentIndex == 0:
            self.sendButton.hide()  # 隐藏发送按钮
            self.searchContactBar.setFocus()  # 搜索框获得焦点
        else:
            self.sendButton.show()  # 显示发送按钮
            self.inputBox.setFocus()  # 文本框获得焦点

    def doubleClickedsearchContactList(self):
        """
        双击搜素结果
        """
        self.getSelectedSearchContactList()
        self.findleContactOnTreeWidget()

    def getSelectedSearchContactList(self):
        """
        获得搜索结果栏选中的目标的id
        """
        self.inputBox.setFocus()  # 文本框获得焦点
        current_searchContactList = repr(self.searchContactList.currentItem())
        if current_searchContactList in self.search_contact_result_dict:
            current_object_info_dict = self.search_contact_result_dict[current_searchContactList]
            current_id = current_object_info_dict['id']
            if self.chat_object_info_dict['id'] != current_id:
                self.chat_object_info_dict = current_object_info_dict
                self.loaded_message_info_dict.clear()
                self.messageList.clear()

    def findleContactOnTreeWidget(self):
        """
        获得联系人列表中被搜索到的的选项
        """
        import handleUiData
        chat_object_info_dict = self.chat_object_info_dict
        current_chat_treewidget_item = None
        current_chat_id = chat_object_info_dict['id']
        current_chat_type = chat_object_info_dict['chat_type']
        current_chat_name = chat_object_info_dict['chat_info_dict']['markname']
        if not current_chat_name:
            current_chat_name = chat_object_info_dict['chat_info_dict']['name']
        if 'friend' in current_chat_type:
            current_chat_treewidget_item = handleUiData.getSelectedSearchTerm(
                current_chat_id, current_chat_name, self.friendTree
            )
            self.friendTree.setCurrentItem(
                curremt_chat_treewidget_item)
            self.contactTabWidget.setCurrentIndex(1)
        # 朋友
        elif 'group' in current_chat_type:
            current_chat_treewidget_item = handleUiData.getSelectedSearchTerm(
                current_chat_id, current_chat_name, self.groupTree
            )
            self.groupTree.setCurrentItem(
                curremt_chat_treewidget_item)
            self.contactTabWidget.setCurrentIndex(2)
        # 群组
        return current_chat_treewidget_item

    def getSelectedSearchTerm(self, current_chat_id, current_chat_name, currcontactTreeWidget):
        current_chat_treewidget_item = None
        current_chat_treewidget_item_list = currcontactTreeWidget.findItems(
            current_chat_name, Qt.MatchExactly | Qt.MatchContains | Qt.MatchRecursive)
        if current_chat_treewidget_item_list:
            for tmp_treewidget_item in current_chat_treewidget_item_list:
                tmp_treewidget_item_str = repr(tmp_treewidget_item)
                friendTree_widget_dict = self.friendTree_widget_dict
                if tmp_treewidget_item_str in friendTree_widget_dict:
                    if current_chat_id == friendTree_widget_dict[tmp_treewidget_item_str]['id']:
                        current_chat_treewidget_item = tmp_treewidget_item
        return current_chat_treewidget_item

    def searchContactBarTextEdited(self):
        """
        去除搜索词汇中的空格
        """
        import re
        self.searchContactList.clear()
        search_text = self.searchContactBar.text()
        search_text = re.sub('\s+', '', search_text)
        if search_text:
            self.search_text = search_text
            self.showSearchContactObject()

    def showSearchContactObject(self):
        """
        搜索所有联系人(包括好友, 群组)
        """
        import handleUiData
        self.search_contact_result_dict.clear()
        search_text = self.search_text
        search_type_list = ['friend', 'group_all']
        friend_info_dict_list = self.friend_info_dict_list
        # 获取好友信息
        group_info_dict_list = self.group_info_dict_list
        # 获取群组信息
        search_dict_list = [friend_info_dict_list, group_info_dict_list]
        # 打包信息
        Search = searchInfo.SearchInfo(
            search_text, search_type_list, search_dict_list)
        search_result_list = Search.searchContactObject()
        # 搜索
        if search_dict_list:
            for tmp_chat_object_info_dict in search_result_list:
                newItem, chat_object_info_dict = handleUiData.handleSearchOutput(
                    tmp_chat_object_info_dict, is_child=False)
                self.search_contact_result_dict[repr(
                    newItem)] = chat_object_info_dict
                self.searchContactList.insertItem(0, newItem)
                # 显示群组基本信息
                if tmp_chat_object_info_dict['search_group_nember_dict_list']:
                    search_result_list = tmp_chat_object_info_dict['search_group_nember_dict_list']
                    for tmp_chat_object_info_dict in search_result_list:
                        newItem, chat_object_info_dict = handleUiData.handleSearchOutput(
                            tmp_chat_object_info_dict, is_child=True)
                        self.search_contact_result_dict[repr(
                            newItem)] = chat_object_info_dict
                        self.searchContactList.insertItem(0, newItem)
                        # 显示组员信息
        # 显示

    def messageNotification(self):
        """
        显示系统级消息提醒
        """
        if self.all_message_dict and 'message_notification_list' in self.all_message_dict:
            message_notification_list = self.all_message_dict['message_notification_list']
            del self.all_message_dict['message_notification_list']
            chat_object_info_dict = self.chat_object_info_dict
            for single_message_dict in message_notification_list:
                if self.isActiveWindow():
                    # 判断为活动窗口
                    chat_object_info_dict = self.chat_object_info_dict
                    sender_id = single_message_dict['sender_id']
                    group_id = single_message_dict['group_id']
                    chat_type = chat_object_info_dict['chat_type']
                    chat_id = chat_object_info_dict['id']
                    if not group_id and chat_type == 'friend' and chat_id == sender_id:
                        # 判断为正在聊天的好友
                        pass
                    elif group_id and chat_type == 'group' and chat_id == group_id:
                        # 判断为正在聊天的群组
                        pass
                    else:
                        group_name = single_message_dict['group_name']
                        if group_name:
                            sender_name = group_name
                        else:
                            friend_name = single_message_dict['sender_name']
                            sender_name = friend_name
                        message_content = single_message_dict['message_content']
                        self.ti.showMessage(
                            sender_name, message_content, self.ti.icon)
                else:
                    group_name = single_message_dict['group_name']
                    if group_name:
                        sender_name = group_name
                    else:
                        friend_name = single_message_dict['sender_name']
                        sender_name = friend_name
                    message_content = single_message_dict['message_content']
                    self.ti.showMessage(
                        sender_name, message_content, self.ti.icon)

    def clickFriendTree(self):
        """
        获取选中的好友ID
        """
        self.inputBox.setFocus()  # 文本框获得焦点
        #  self.groupTree.clearSelection()
        current_friendTree = repr(self.friendTree.currentItem())
        if current_friendTree in self.friendTree_widget_dict:
            current_object_info_dict = self.friendTree_widget_dict[current_friendTree]
            current_id = current_object_info_dict['id']
            if self.chat_object_info_dict['id'] != current_id:
                self.chat_object_info_dict['id'] = self.friendTree_widget_dict[current_friendTree]['id']
                self.chat_object_info_dict['chat_type'] = 'friend'
                self.chat_object_info_dict['chat_info_dict'] = current_object_info_dict
                self.loaded_message_info_dict.clear()
                self.messageList.clear()

    def clickGroupTree(self):
        """
        获取选中的群组ID
        """
        self.inputBox.setFocus()  # 文本框获得焦点
        #  self.friendTree.clearSelection()
        current_groupTree = repr(self.groupTree.currentItem())
        if current_groupTree in self.groupTree_widget_dict:
            current_object_info_dict = self.groupTree_widget_dict[current_groupTree]
            current_id = current_object_info_dict['id']
            if self.chat_object_info_dict['id'] != current_id:
                self.chat_object_info_dict['id'] = current_id
                self.chat_object_info_dict['chat_type'] = 'group'
                self.chat_object_info_dict['chat_info_dict'] = current_object_info_dict
                self.loaded_message_info_dict.clear()
                self.messageList.clear()

    def loadFriendTree(self):
        """
        载入好友列表
        """
        friend_info_list = getInfo.getFriendInfo()  # 获取好友列表
        if friend_info_list and self.friend_info_dict_list != friend_info_list:
            self.friend_info_dict_list = friend_info_list
            friend_category_list = list(
                set([tmp_dict['category'] for tmp_dict in friend_info_list]))
            self.friendTree.setsortingenabled = True
            self.friendTree_widget_dict.clear()
            self.friendTree.clear()  # 清空联系人列表
            for friend_category in friend_category_list:
                treecategory = QTreeWidgetItem([friend_category])
                for single_friend_info_list in friend_info_list:
                    friend_markname = single_friend_info_list['markname']
                    friend_name = single_friend_info_list['name']
                    if not friend_markname:
                        friend_markname = friend_name
                    if single_friend_info_list['category'] == friend_category:
                        if not friend_markname:
                            friend_markname = friend_name
                        friend_tree_info = QTreeWidgetItem([friend_markname])
                        friend_tree_info.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        self.friendTree_widget_dict[repr(
                            friend_tree_info)] = single_friend_info_list
                        treecategory.addChild(friend_tree_info)
                        treecategory.setExpanded(True)
                        # 自动展开联系人
                        # TODO: 保持联系人展开信息
                treecategory.setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.friendTree.addTopLevelItem(treecategory)
                # 完成分类的联系人绘制

    def loadGroupTree(self):
        """
        载入群组列表
        """
        group_info_list = getInfo.getGroupInfo()  # 获取群组信息
        if group_info_list and self.group_info_dict_list != group_info_list:
            self.group_info_dict_list = group_info_list
            for friend_category in ['未分类']:
                # TODO: 完成本地分类并存储本地功能
                treecategory = QTreeWidgetItem([friend_category])
                for single_group_info_dict in group_info_list:
                    group_markname = single_group_info_dict['markname']
                    group_name = single_group_info_dict['name']
                    if not group_markname:
                        group_markname = group_name
                        group_tree_info = QTreeWidgetItem([group_markname])
                        group_tree_info.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        self.groupTree_widget_dict[repr(
                            group_tree_info)] = single_group_info_dict
                        treecategory.addChild(group_tree_info)
                        treecategory.setExpanded(True)
                treecategory.setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.groupTree.addTopLevelItem(treecategory)

    def loadMessageList(self):
        """
        载入消息列表
        """
        if self.chat_object_info_dict['id']:
            chat_object_id = self.chat_object_info_dict['id']
            if chat_object_id in self.all_message_dict:
                message_list = self.all_message_dict[chat_object_id]
                for single_message_dict in message_list:
                    if single_message_dict not in self.loaded_message_info_dict.values():
                        message_content = single_message_dict['message_content']
                        newMessage = QtWidgets.QListWidgetItem()
                        newMessage.setText(message_content)
                        self.loaded_message_info_dict[repr(
                            newMessage)] = single_message_dict
                        self.messageListWidget.addItem(newMessage)
                        self.messageListWidget.scrollToBottom()

    def getSendText(self):
        """
        发送键按下后获取输入框文本并清空
        """
        send_text = self.inputBox.toPlainText()
        if not len(send_text):
            send_text = None
        return send_text

    def sendMessage(self):
        """
        发送消息
        """
        self.inputBox.setFocus()  # 文本框获得焦点
        receiver_id = self.chat_object_info_dict['id']
        send_text = self.getSendText()
        if receiver_id and send_text:
            self.inputBox.clear()
            chat_type = self.chat_object_info_dict['chat_type']
            if chat_type == 'friend':
                sendMessage.sendFriendMessage(receiver_id, send_text)
            elif chat_type == 'group':
                sendMessage.sendGroupMessage(receiver_id, send_text)


def main(friend_message_dict, post_data_list):
    app = QtWidgets.QApplication(sys.argv)
    ui = MainPage(friend_message_dict, post_data_list)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
