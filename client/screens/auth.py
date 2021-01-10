from PyQt5.QtWidgets import QMainWindow
from ui.auth import Ui_MainWindow

from screens.chat import ChatScreen

class AuthScreen(QMainWindow, Ui_MainWindow):
    def __init__(self, ws=None):
        super(AuthScreen, self).__init__(ws)
        self.ws = ws
        self.setupUi(self)

        #self.loginButton.clicked.connect(self.ws.connect_ws)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        if not self.inputName.text():
            self.errorText.setStyleSheet("color: #7F0000;")
            self.errorText.setText('Не указано имя')
            return
        elif not self.inputPassword.text():
            self.errorText.setStyleSheet("color: #7F0000;")
            self.errorText.setText('Не указан пароль')
            return
        elif not self.URLInput.text():
            self.errorText.setStyleSheet("color: #7F0000;")
            self.errorText.setText('Не указан сервер')
            return
        else:
            self.errorText.setStyleSheet("color: #007F00;")
            self.errorText.setText('Подключение к серверу...')

        self.ws.connect_ws()