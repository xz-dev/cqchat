# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1208, 819)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(5, 4, 1205, 763))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.friendTree = QtWidgets.QTreeWidget(self.layoutWidget)
        self.friendTree.setMinimumSize(QtCore.QSize(261, 451))
        self.friendTree.setObjectName("friendTree")
        self.verticalLayout_2.addWidget(self.friendTree)
        self.groupTree = QtWidgets.QTreeWidget(self.layoutWidget)
        self.groupTree.setObjectName("groupTree")
        self.verticalLayout_2.addWidget(self.groupTree)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageList = QtWidgets.QListWidget(self.layoutWidget)
        self.messageList.setMinimumSize(QtCore.QSize(931, 721))
        self.messageList.setObjectName("messageList")
        self.verticalLayout.addWidget(self.messageList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputBox = QtWidgets.QTextEdit(self.layoutWidget)
        self.inputBox.setMinimumSize(QtCore.QSize(840, 30))
        self.inputBox.setMaximumSize(QtCore.QSize(840, 30))
        self.inputBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.inputBox.setObjectName("inputBox")
        self.horizontalLayout.addWidget(self.inputBox)
        self.sendButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sendButton.setMinimumSize(QtCore.QSize(84, 30))
        self.sendButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1208, 30))
        self.menubar.setObjectName("menubar")
        self.menuWebQQ_Python = QtWidgets.QMenu(self.menubar)
        self.menuWebQQ_Python.setObjectName("menuWebQQ_Python")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuWebQQ_Python.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WebQQ-Python"))
        self.friendTree.headerItem().setText(0, _translate("MainWindow", "好友"))
        self.groupTree.headerItem().setText(0, _translate("MainWindow", "群组"))
        self.inputBox.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>输入</p></body></html>"))
        self.sendButton.setText(_translate("MainWindow", "发送"))
        self.menuWebQQ_Python.setTitle(_translate("MainWindow", "WebQQ-&Python"))

