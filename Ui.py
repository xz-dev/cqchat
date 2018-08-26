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
    def __init__(self, all_message_dict):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super().__init__()
        self.all_message_dict = all_message_dict
        self.loaded_message_info_dict = dict()
        self.friendTree_widget_dict = dict()
        self.groupTree_widget_dict = dict()
        self.chat_object_id = 0
        self.friend_info_list = list()
        self.group_info_list = list()
        self.sendId = None
        self.setupUi(self)
        self.loadFriendTree()  # 绘出好友列表
        self.loadGroupTree()  # 绘出群组列表
        #  self.friendTree.itemDoubleClicked.connect(self.getSendText)
        #  newPeople = QtWidgets.QListWidgetItem()
        #  newPeople.setText("HI")
        #  self.friendTree.insertItem(4, newPeople)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.autoRefreshData)
        self.timer.start(100)
        #  self.timer.timeout.connect(self.loadFriendTree)
        #  self.timer.start(300000)  # 每五分钟刷新一次联系人
        # TODO: 整合所有定时刷新函数
        self.sendButton.clicked.connect(self.sendMessage)  # 调取发送函数
        self.friendTree.clicked.connect(self.loadMessageList)

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
        #  for frienfname in friendTree:
        #      qtwidgets.qlistwidgetitem(frienfname, self.friendTree)
        #  rowfriendTree = self.peoplelist.count()
        #  newpeople = qtwidgets.qlistwidgetitem()
        # 将好友名字写入列表

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
        chat_object_id = self.getSelectedId()
        if chat_object_id != self.chat_object_id:
            self.messageList.clear()
            self.chat_object_id = chat_object_id
        if chat_object_id in self.all_message_dict:
            message_list = self.all_message_dict[chat_object_id]
            for single_message_dict in message_list:
                if single_message_dict not in self.loaded_message_info_dict.values():
                    message_content = single_message_dict['message_content']
                    print(message_content)
                    #  message_time = time.strftime(
                    #      "%Y-%m-%d %H:%M:%S", time.localtime(message_unit_time))
                    #  message = message_time + '|' + \
                    #      "{:<{x}}".format(sender_name, x=20) + message_content
                    newMessage = QtWidgets.QListWidgetItem()
                    newMessage.setText(message_content)
                    self.loaded_message_info_dict[repr(
                        newMessage)] = single_message_dict
                    self.messageList.addItem(newMessage)
                    self.messageList.scrollToBottom()
                    #  self.messaglast_time = int(message_unit_time)
                    # 时间戳是str类型
                    #  message_rows = self.messageList.count()
                    #  if message_rows:
                    #      message_rows = list(range(self.messageList.count()))[-1]
                    #      if message != self.messageList.item(message_rows).text():
                    #          self.messageList.addItem(newMessage)
                    #  else:
                    #      self.messageList.addItem(newMessage)

                    #  for index in range(self.messageList.count()):
                    #      print(self.messageList.item(index).text())
            #      QtWidgets.QListWidgetItem(message, self.messageList)
            #  row_message_list = self.messageList.count()
            #  new_message = QtWidgets.QListWidgetItem()

    def getSelectedId(self):
        """
        获取当前选中的联系人
        """
        #  hititem = self.friendTree.currentitem()
        #  textlist = list()
        #  for ix in self.friendTree.selectedIndexes():
        #      text = ix.data()
        #      textlist.append(text)
        #  if len(textlist) != 0:
        #      sendid = textlist[-1]
        current_friendTree = repr(self.friendTree.currentItem())
        if current_friendTree in self.friendTree_widget_dict:
            sendid = self.friendTree_widget_dict[current_friendTree]['id']
            return sendid
        else:
            return None

    def getSendText(self):
        """
        发送键按下后获取输入框文本并清空
        """
        #  self.friendTree.sortltems()
        #  del_ = self.friendTree.selecteditems
        #  del_item = self.takeitem(self.row(del_))
        send_text = self.inputBox.toPlainText()
        if len(send_text):
            self.inputBox.clear()
        else:
            send_text = None
        return send_text

    def sendMessage(self):
        """
        发送消息
        """
        receiver_id = self.getSelectedId()
        send_text = self.getSendText()
        if receiver_id and send_text:
            sendMessage.sendFriendMessage(receiver_id, send_text)


class ShowImage(QWidget):
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
    #  global tmp_friend_message_dict
    #  tmp_friend_message_dict = friend_message_dict
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
