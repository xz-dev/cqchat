import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget, QLabel
import MainGui

import sendMessage
from get import getInfo
import searchInfo

#  from PyQt5.QtWidgets import *
#  from PyQt5.QtCore import *
#  from PyQt5.QtGui import *


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.showMenu()
        self.showIcon()
        self.connectEvent()

    def connectEvent(self):
        self.activated.connect(self.iconClied)
        # 把鼠标点击图标的信号和槽连接

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()

    def showMenu(self):
        self.menu = QMenu()
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

    def showIcon(self):
        self.setIcon(QIcon("./icon/tray_icon.png"))
        self.icon = self.MessageIcon()

    def quit(self):
        "保险起见，为了完整的退出"
        self.setVisible(False)
        self.parent().close()
        qApp.quit()
        sys.exit()


class MainPage(QtWidgets.QMainWindow, MainGui.Ui_MainWindow, QSystemTrayIcon):
    """
    显示主页面
    """

    def __init__(self, all_message_dict, parent=None):
        super().__init__()
        # 系统托盘图标
        super(MainPage, self).__init__(parent)
        self.ti = TrayIcon(self)
        self.ti.show()
        self.all_message_dict = all_message_dict
        self.loaded_message_info_dict = dict()
        self.friendTree_widget_dict = dict()
        self.groupTree_widget_dict = dict()
        self.chat_object_info_dict = {'id': None, 'chat_type': None}
        self.friend_info_dict_list = list()
        self.group_info_list = list()
        self.search_contact_result_dict = dict()  # 搜索所有联系人结果字典
        # friend_info_list 与 group_info_list只做备份列表用于查看是否有更改
        # TODO: 监控POST以实时调整信息
        self.setupUi(self)
        self.loadFriendTree()  # 绘出好友列表
        self.loadGroupTree()  # 绘出群组列表
        #  self.timer.timeout.connect(self.loadFriendTree)
        #  self.timer.start(300000)  # 每五分钟刷新一次联系人
        self.autoRefreshData()
        # TODO: 整合所有定时刷新函数
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
        self.timer1.timeout.connect(self.loadMessageList)
        self.timer1.start(50)
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.messageNotification)
        self.timer2.start(50)

    def trayMenu(self):
        """
        系统托盘
        """
        self.quitAction = QAction("退出", self, triggered=self.quit)
        # 系统托盘退出菜单

    def clickContactTabWidget(self):
        currentIndex = self.contactTabWidget.currentIndex()
        if currentIndex == 0:
            self.searchContactBar.setFocus()  # 搜索框获得焦点
        else:
            self.inputBox.setFocus()  # 文本框获得焦点

    def findleContactOnTreeWidget(self):
        """
        获得联系人列表中被搜索到的的选项
        """
        chat_object_info_dict = self.chat_object_info_dict
        curremt_chat_treewidget_item = None
        curremt_chat_id = chat_object_info_dict['id']
        current_chat_type = chat_object_info_dict['chat_type']
        current_chat_name = chat_object_info_dict['chat_info_dict']['markname']
        if not current_chat_name:
            current_chat_name = chat_object_info_dict['chat_info_dict']['name']
        if current_chat_type == 'friend':
            curremt_chat_treewidget_item_list = self.friendTree.findItems(
                current_chat_name, Qt.MatchExactly | Qt.MatchContains | Qt.MatchRecursive)
            if curremt_chat_treewidget_item_list:
                for tmp_treewidget_item in curremt_chat_treewidget_item_list:
                    tmp_treewidget_item_str = repr(tmp_treewidget_item)
                    friendTree_widget_dict = self.friendTree_widget_dict
                    if tmp_treewidget_item_str in friendTree_widget_dict:
                        if curremt_chat_id == friendTree_widget_dict[tmp_treewidget_item_str]['id']:
                            curremt_chat_treewidget_item = tmp_treewidget_item
                            self.friendTree.setCurrentItem(
                                curremt_chat_treewidget_item)
                            self.contactTabWidget.setCurrentIndex(1)
        elif current_chat_type == 'group':
            curremt_chat_treewidget_item_list = self.groupTree.findItems(
                current_chat_name, Qt.MatchExactly | Qt.MatchContains | Qt.MatchRecursive)
            if curremt_chat_treewidget_item_list:
                for tmp_treewidget_item in curremt_chat_treewidget_item_list:
                    tmp_treewidget_item_str = repr(tmp_treewidget_item)
                    groupTree_widget_dict = self.groupTree_widget_dict
                    if tmp_treewidget_item_str in groupTree_widget_dict:
                        if curremt_chat_id == groupTree_widget_dict[tmp_treewidget_item_str]['id']:
                            curremt_chat_treewidget_item = tmp_treewidget_item
                            self.groupTree.setCurrentItem(
                                curremt_chat_treewidget_item)
                            self.contactTabWidget.setCurrentIndex(2)
        return curremt_chat_treewidget_item

    def doubleClickedsearchContactList(self):
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

    def searchContactBarTextEdited(self):
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
        self.search_contact_result_dict.clear()
        search_text = self.search_text
        friend_info_dict_list = self.friend_info_dict_list
        search_dict_list = friend_info_dict_list
        search_result_list = searchInfo.searchContactObject(
            search_text, search_dict_list)
        if search_dict_list:
            for tmp_chat_object_info_dict in search_result_list:
                search_contact_text = None
                search_chat_object_name = None
                tmp_search_text_list = tmp_chat_object_info_dict['search_text_list']
                tmp_chat_object_info_dict = tmp_chat_object_info_dict['search_dict']
                if tmp_chat_object_info_dict['markname']:
                    search_chat_object_name = tmp_chat_object_info_dict['markname']
                else:
                    search_chat_object_name = tmp_chat_object_info_dict['name']
                for search_text in tmp_search_text_list:
                    if not search_contact_text:
                        search_contact_text = search_chat_object_name
                    if search_text != search_chat_object_name:
                        search_contact_text = search_contact_text + '\n' + search_text
                newItem = QtWidgets.QListWidgetItem()
                newItem.setText(search_contact_text)
                chat_object_info_dict = dict()
                chat_object_info_dict['id'] = tmp_chat_object_info_dict['id']
                chat_object_info_dict['chat_type'] = 'friend'
                chat_object_info_dict['chat_info_dict'] = tmp_chat_object_info_dict
                self.search_contact_result_dict[repr(
                    newItem)] = chat_object_info_dict
                self.searchContactList.insertItem(0, newItem)

    def messageNotification(self):
        """
        显示系统级消息提醒
        """
        if 'message_notification_list' in self.all_message_dict:
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
        if self.friend_info_dict_list != friend_info_list:
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
        if self.group_info_list != group_info_list:
            self.group_info_list = group_info_list
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
                        self.messageList.addItem(newMessage)
                        self.messageList.scrollToBottom()

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


class ShowImage(QWidget):
    """
    显示二维码
    """

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.autoClose)
        self.timer.start(100)
        self.title = 'QrCode'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        pixmap = QtGui.QPixmap(self.image_path)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()

    def autoClose(self):
        if not os.path.exists(self.image_path):
            self.close()


def main(friend_message_dict):
    app = QtWidgets.QApplication(sys.argv)
    ui = MainPage(friend_message_dict)
    ui.show()
    sys.exit(app.exec_())


def showQrcode(image_path):
    app = QApplication(sys.argv)
    ex = ShowImage(image_path)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
