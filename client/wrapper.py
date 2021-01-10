from PyQt5 import QtWebSockets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow
import json
import logging

from screens.auth import AuthScreen
from screens.chat import ChatScreen


class WebsocketWrapper(QMainWindow):
    def __init__(self):
        super().__init__()
        # Инициализация QWebSocket и открытие экрана авторизации
        self.ws = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version13, None)
        self.routes = {}

        logging.info('Открытие authScreen')
        self.authScreen = AuthScreen(self)
        self.authScreen.show()

        self.chatScreen = ChatScreen(self)

        # Подключение всех websocket обработчиков
        self.ws.error.connect(self.error)
        self.ws.textMessageReceived.connect(self.message_handler)
        self.ws.pong.connect(self.on_pong)

        self.id = None
        self.url = None
        self.name = None
        self.password = None

    def connect_ws(self):
        self.url = self.authScreen.URLInput.text()
        self.name = self.authScreen.inputName.text()
        self.password = self.authScreen.inputPassword.text()

        self.subscribe_basic_methods()

        logging.info(f'Подключение к Websocket по адресу {self.url}')
        self.ws.open(QUrl(self.url))

    def send_message(self, message):
        message = json.dumps(message)
        logging.info(f'[Out]: {message}')
        self.ws.sendTextMessage(message)

    def message_handler(self, message):
        message = json.loads(message)
        logging.info(f'[In]: {message}')

        if message['method'] in self.routes.keys():
            self.routes[message['method']](message)

    def subscribe(self, method_name, handler):
        # Подписка обработчика на события от бекенда
        self.routes[method_name] = handler

    def subscribe_basic_methods(self):
        self.subscribe('init', lambda x: self.send_message(
            {'method': 'auth', 'data': {'username': self.name, 'password': self.password}}
        ))
        self.subscribe('auth', lambda x: self.auth_handler(x))
        self.subscribe('userChats', lambda x: self.chatScreen.render_chats(x))

    def auth_handler(self, r):
        if not r['success']:
            self.authScreen.errorText.setStyleSheet("color: #7F0000;")
            self.authScreen.errorText.setText('Неверный пароль')
        else:
            # Открываем экран чата
            self.id = r['data']['id']
            self.chatScreen.Form.setWindowTitle(f'Чат - Пользователь {self.name}')
            self.authScreen.errorText.setText('')
            self.authScreen.close()
            self.chatScreen.show()

    def do_ping(self):
        logging.debug('[Out]: Ping')
        self.ws.ping(b"foo")

    def on_pong(self, elapsedTime, payload):
        logging.debug('[In]: Pong')
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))

    def error(self, error_code):
        logging.critical("Websocket error code: {}".format(error_code))
        logging.critical("Websocket status: {}".format(self.ws.errorString()))

        self.authScreen.errorText.setStyleSheet("color: #7F0000;")
        if int(error_code) == 1:
            self.authScreen.errorText.setText('Потеряно соединение с сервером')
            self.chatScreen.close()
            self.authScreen.show()
        elif int(error_code) == 0:
            self.authScreen.errorText.setText('Сервер не отвечает')
        elif int(error_code) == 2:
            self.authScreen.errorText.setText('Хост не найден')
        else:
            self.authScreen.errorText.setText(self.ws.errorString())