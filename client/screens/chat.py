from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5.QtGui import QFont
from ui.chat import Ui_Form
from ui.createChat import Ui_CreateChat
from ui.joinChat import Ui_JoinChat


class CreateChatModal(QMainWindow, Ui_CreateChat):
    def __init__(self, parent):
        super(CreateChatModal, self).__init__(parent)
        self.ws = parent.ws
        self.setupUi(self)

        self.errorText.setText('')
        self.createButton.clicked.connect(self.create_chat)

    def create_chat(self):
        title = self.chatTitle.text()
        self.ws.subscribe('createChat', self.response_handler)
        self.ws.send_message({'method': 'createChat', 'data': {'name': title}})

    def response_handler(self, r):
        if r['success']:
            self.errorText.setStyleSheet("color: #007F00;")
            self.errorText.setText('Чат успешно создан')
        else:
            self.errorText.setStyleSheet("color: #7F0000;")
            self.errorText.setText(r['text'])


class JoinChatModal(QMainWindow, Ui_JoinChat):
    def __init__(self, parent):
        super(JoinChatModal, self).__init__(parent)
        self.ws = parent.ws
        self.setupUi(self)
        self.joinButton.clicked.connect(self.join_chat)

    def join_chat(self):
        self.ws.subscribe('joinChat', self.response_handler)
        self.ws.send_message({'method': 'joinChat', 'data': {'invite_code': self.inviteCode.text()}})

    def response_handler(self, r):
        if r['success']:
            self.errorText.setStyleSheet("color: #007F00;")
            self.errorText.setText('Вы успешно присоединились к чату')
        else:
            self.errorText.setStyleSheet("color: #7F0000;")
            self.errorText.setText(r['text'])


class ChatScreen(QMainWindow, Ui_Form):
    def __init__(self, ws=None):
        super(ChatScreen, self).__init__(ws)

        self.ws = ws
        self.selectedChat = None
        self.messages_by_chat = {}
        self.need_render = False

        self.setupUi(self)
        self.createChatModal = CreateChatModal(self)
        self.joinChatModal = JoinChatModal(self)

        self.register_handlers()

    def register_handlers(self):
        self.ws.subscribe('newMessage', self.newMessage_handler)
        self.userChats.itemClicked.connect(self.onclick_chat)

        # Обработчики для кнопки создания чата
        self.createChat_button.clicked.connect(lambda: [
            self.createChatModal.errorText.setText(''),
            self.createChatModal.show()
        ])

        # Обработчики для кнопки вступления в чат
        self.joinChat_button.clicked.connect(lambda: [
            self.joinChatModal.errorText.setText(''),
            self.joinChatModal.show()
        ])

        # Enter и кнопка отправки сообщения
        self.sendButton.clicked.connect(self.send_message)
        self.messageInput.returnPressed.connect(self.send_message)

    def render_chats(self, r):
        # Отображение списка всех чатов
        chats = r['data']
        self.userChats.clear()
        for chat in chats:
            item = QListWidgetItem()
            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setText(chat['name'])
            item.setWhatsThis(str(chat['id']))
            self.userChats.addItem(item)

    def newMessage_handler(self, r):
        chat_id = r['data'][1]
        if chat_id not in self.messages_by_chat.keys():
            # Если мы ещё не выгружали историю чата, то выгружаем сейчас
            self.get_history(chat_id)
            self.need_render = self.selectedChat == chat_id
            return

        # Добавляем сообщение к общему списку
        self.messages_by_chat[chat_id].append(r['data'])

        # Если на данный момент у пользователя открыт этот чат,
        # то делаем ререндер сообщений в нём
        if self.selectedChat == chat_id:
            self.render_messages(chat_id)

    def get_messages(self, r):
        chat_id = int(r['data'][0][1])
        self.messages_by_chat[chat_id] = r['data']
        if self.need_render:
            self.render_messages(chat_id)

    def render_messages(self, chat_id):
        # Рендеринг всех сообщений

        if chat_id not in self.messages_by_chat.keys():
            # Если мы ещё не выгружали историю чата, то выгружаем сейчас
            self.get_history(chat_id)
            self.need_render = True
            return

        messages = self.messages_by_chat[chat_id]
        result = ''

        for msg in messages:
            date = msg[2].split(" ")[1]
            result += f'[{date}] <{msg[3]}>: {msg[4]}\n'

        # Обновляем браузер и скроллим его в самый низ
        self.chatBrowser.setText(result)
        scroll = self.chatBrowser.verticalScrollBar()
        scroll.setValue(scroll.maximum())
        self.need_render = False

    def get_history(self, chat_id):
        self.ws.subscribe('messages', self.get_messages)
        self.ws.send_message({'method': 'messages', 'chat_id': chat_id})

    def onclick_chat(self, item):
        self.selectedChat = int(item.whatsThis())
        self.render_messages(self.selectedChat)

    def send_message(self):
        if self.selectedChat and self.messageInput.text():
            self.ws.send_message({'method': 'send', 'data': {
                'chat_id': self.selectedChat,
                'msg': self.messageInput.text()
            }})
            self.messageInput.setText('')