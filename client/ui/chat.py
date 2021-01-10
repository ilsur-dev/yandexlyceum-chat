from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 595)
        Form.setFixedSize(1105, 595)
        self.Form = Form
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1101, 591))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(3, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.createChat_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createChat_button.sizePolicy().hasHeightForWidth())
        self.createChat_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.createChat_button.setFont(font)
        self.createChat_button.setObjectName("createChat_button")
        self.verticalLayout_2.addWidget(self.createChat_button)
        self.joinChat_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.joinChat_button.setFont(font)
        self.joinChat_button.setObjectName("joinChat_button")
        self.verticalLayout_2.addWidget(self.joinChat_button)
        self.userChats = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.userChats.setObjectName("userChats")
        self.verticalLayout_2.addWidget(self.userChats)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.chatBrowser = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chatBrowser.setFont(font)
        self.chatBrowser.setObjectName("chatBrowser")
        self.verticalLayout.addWidget(self.chatBrowser)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.messageInput = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.messageInput.setFont(font)
        self.messageInput.setText("")
        self.messageInput.setObjectName("messageInput")
        self.horizontalLayout_3.addWidget(self.messageInput)
        self.sendButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendButton.setFont(font)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout_3.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Chat"))
        self.createChat_button.setText(_translate("Form", "Создать чат"))
        self.joinChat_button.setText(_translate("Form", "Войти в чат"))
        __sortingEnabled = self.userChats.isSortingEnabled()
        self.userChats.setSortingEnabled(False)
        #item = self.userChats.item(0)
        #item.setText(_translate("Form", "Яндекс лицей"))
        self.userChats.setSortingEnabled(__sortingEnabled)
        self.sendButton.setText(_translate("Form", "Отправить"))
