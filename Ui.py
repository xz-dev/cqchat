import sys
import time
import os
from PyQt5.QtWidgets import QApplication, QWidget
#  from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget, QLabel
from gui import MainGui

import sendMessage
from get import getInfo
from post import postServer


class MainPage(QtWidgets.QMainWindow, MainGui.Ui_MainWindow):
    """
    显示主页面
    """

    def __init__(self, all_message_dict):
        super().__init__()
        self.all_message_dict = all_message_dict
        self.loaded_message_info_dict = dict()
        self.friendTree_widget_dict = dict()
        self.groupTree_widget_dict = dict()
        self.chat_object_info_dict = {'id':None, 'chat_type': None}
        self.friend_info_list = list()
        self.group_info_list = list()
        # friend_info_list 与 group_info_list只做备份列表用于查看是否有更改
        # TODO: 监控POST以实时调整信息
        self.setupUi(self)
        self.loadFriendTree()  # 绘出好友列表
        self.loadGroupTree()  # 绘出群组列表
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.autoRefreshData)
        self.timer.start(50)
        #  self.timer.timeout.connect(self.loadFriendTree)
        #  self.timer.start(300000)  # 每五分钟刷新一次联系人
        # TODO: 整合所有定时刷新函数
        self.sendButton.clicked.connect(self.sendMessage)  # 调取发送函数
        #  self.friendTree.clicked.connect(self.loadMessageList)  # 自动载入消息列表
        self.friendTree.clicked.connect(self.clickFriendTree) # 获取选中的好友ID
        self.groupTree.clicked.connect(self.clickGroupTree) # 获取选中的群组ID

    def clickFriendTree(self):
        """
        获取选中的好友ID
        """
        self.groupTree.clearSelection()
        current_friendTree = repr(self.friendTree.currentItem())
        if current_friendTree in self.friendTree_widget_dict:
            current_id = self.friendTree_widget_dict[current_friendTree]['id']
            if self.chat_object_info_dict['id'] != current_id:
                self.chat_object_info_dict['id'] = self.friendTree_widget_dict[current_friendTree]['id']
                self.chat_object_info_dict['chat_type'] = 'friend'
                self.loaded_message_info_dict.clear()
                self.messageList.clear()
            #  return sendid

    def clickGroupTree(self):
        """
        获取选中的群组ID
        """
        self.friendTree.clearSelection()
        current_groupTree = repr(self.groupTree.currentItem())
        if current_groupTree in self.groupTree_widget_dict:
            current_id = self.groupTree_widget_dict[current_groupTree]['id']
            if self.chat_object_info_dict['id'] != current_id:
                self.chat_object_info_dict['id'] = current_id
                self.chat_object_info_dict['chat_type'] = 'group'
                self.loaded_message_info_dict.clear()
                self.messageList.clear()
                #  return sendid

    def getSelectedId(self):
        """
        获取当前选中的联系人
        """
        current_friendTree = repr(self.friendTree.currentItem())
        if current_friendTree in self.friendTree_widget_dict:
            sendid = self.friendTree_widget_dict[current_friendTree]['id']
            return sendid
        else:
            return None

    def autoRefreshData(self):
        self.loadMessageList()  # 自动刷新一次消息列表

    def loadFriendTree(self):
        """
        载入好友列表
        """
        friend_info_list = getInfo.getFriendInfo()  # 获取好友列表
        if self.friend_info_list != friend_info_list:
            self.friend_info_list = friend_info_list
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
                        self.friendTree_widget_dict[repr(
                            friend_tree_info)] = single_friend_info_list
                        treecategory.addChild(friend_tree_info)
                        treecategory.setExpanded(True)
                        # 自动展开联系人
                        # TODO: 保持联系人展开信息
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
                        self.groupTree_widget_dict[repr(
                            group_tree_info)] = single_group_info_dict
                        treecategory.addChild(group_tree_info)
                        treecategory.setExpanded(True)
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
