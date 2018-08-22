import sys
import os
import multiprocessing as mp
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget
from gui import MainGui

import message
from get import getInfo
from post import postServer


class MainPage(QtWidgets.QMainWindow, MainGui.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super().__init__()
        self.sendId = None
        self.setupUi(self)
        self.makeFriendNameList()  # 绘出好友列表
        #  self.peopleList.itemDoubleClicked.connect(self.getSendText)
        #  newPeople = QtWidgets.QListWidgetItem()
        #  newPeople.setText("HI")
        #  self.peopleList.insertItem(4, newPeople)

        self.sendButton.clicked.connect(self.sendMessage)  # 调取发送函数

    def makeFriendNameList(self):
        self.peopleList.clear()  # 清空联系人列表
        peopleinfo = getInfo.getFriendInfo()  # 获取好友列表
        peopleList, categorylist = getInfo.getName(peopleinfo)
        self.peopleList.setsortingenabled = True
        for category in categorylist:
            treecategory = QTreeWidgetItem([category])
            for tempid in peopleList.keys():
                if peopleList[tempid]['category'] == category:
                    treepeopleinfo = QTreeWidgetItem([peopleList[tempid]['name'],
                                                      str(tempid)])
                    treecategory.addChild(treepeopleinfo)
                    treecategory.setExpanded(True)
                    # 自动展开联系人
                    # todo: 保持联系人展开信息
            self.peopleList.addTopLevelItem(treecategory)
            # 完成分类的联系人绘制
        #  for frienfname in peopleList:
        #      qtwidgets.qlistwidgetitem(frienfname, self.peopleList)
        #  rowpeopleList = self.peoplelist.count()
        #  newpeople = qtwidgets.qlistwidgetitem()
        # 将好友名字写入列表

    def getSendId(self):
        #  hititem = self.peopleList.currentitem()
        textlist = list()
        for ix in self.peopleList.selectedIndexes():
            text = ix.data()
            textlist.append(text)
        if len(textlist) != 0:
            sendid = textlist[-1]
            return sendid
        else:
            return none

    def getSendText(self):
        """
        发送键按下后获取输入框文本并清空
        """
        #  self.peopleList.sortltems()
        #  del_ = self.peopleList.selecteditems
        #  del_item = self.takeitem(self.row(del_))
        sendtext = self.inputBox.toPlainText()
        self.inputBox.clear()
        return sendtext

    def sendMessage(self):
        """
        发送消息
        """
        message.sendFriendMessage(self.getSendId(), self.getSendText())



def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MainPage()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#  resp = message.sendfriendmessage('zero', content)
#  issuccess = message.issuccess(resp)
#  if issuccess:
#      print("发送成功")
