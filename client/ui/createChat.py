# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createChat.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateChat(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 244)
        MainWindow.setFixedSize(452, 244)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("Создание чата")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(170, 30, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setKerning(True)
        self.title.setFont(font)
        self.title.setAccessibleName("")
        self.title.setAccessibleDescription("")
        self.title.setObjectName("title")
        self.chatTitle = QtWidgets.QLineEdit(self.centralwidget)
        self.chatTitle.setGeometry(QtCore.QRect(100, 100, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.chatTitle.setFont(font)
        self.chatTitle.setText("")
        self.chatTitle.setObjectName("chatTitle")
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(100, 140, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createButton.setFont(font)
        self.createButton.setObjectName("createButton")
        self.errorText = QtWidgets.QLabel(self.centralwidget)
        self.errorText.setGeometry(QtCore.QRect(100, 180, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.errorText.setFont(font)
        self.errorText.setText("")
        self.errorText.setObjectName("errorText")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.title.setText(_translate("MainWindow", "Создать чат"))
        self.chatTitle.setPlaceholderText(_translate("MainWindow", "Название чата"))
        self.createButton.setText(_translate("MainWindow", "Создать"))