import logging
from random import choices, randint
from hashlib import sha256
from time import sleep
import json

# Специально уменьшенный алфавит :)
random_invite_code = lambda x: ''.join(choices('ABDFHKMPZRTXYZ', k=x))

# Хеширование паролей в базе данных
get_hash = lambda x: sha256(x.encode('utf8')).hexdigest()
password_salt = 'yandex'


class User:
    def __init__(self, websocket, database, clients):
        self.ws = websocket
        self.db = database
        self.clients = clients
        self.id = None
        self.name = None
        self.chats = None

    async def listen_messages(self):
        await self.ws.send(json.dumps({'method': 'init', 'message': 'requiredAuth'}))
        async for message in self.ws:
            message = json.loads(message)
            await self.router(message)

        # При отключении клиента удаляем его
        self.clients.remove_client(self)

    async def router(self, message):
        logging.info(f'Новое сообщение: {message["method"]}')

        if message['method'] == 'auth':
            await self.handler_auth(message['data'])
        elif message['method'] == 'userChats':
            await self.handler_userChats()
        elif message['method'] == 'joinChat':
            await self.handler_joinChat(message['data']['invite_code'])
        elif message['method'] == 'createChat':
            await self.handler_createChat(message['data'])
        elif message['method'] == 'messages':
            await self.handler_getMessages(message['chat_id'])
        elif message['method'] == 'send':
            await self.handler_send(message['data'])

    async def handler_userChats(self):
        # Получение всех чатов пользователя и отправка
        chats = self.db.cur.execute('''
            SELECT uc.chat_id, c.name, uc.entry_date FROM user_chats uc
            INNER JOIN chats c ON uc.chat_id = c.id
            WHERE uc.user_id = ?
        ''', [self.id]).fetchall()
        self.chats = [{'id': i[0], 'name': i[1], 'entry_date': i[2]} for i in chats]

        # Добавление пользователя в объект онлайна по каждому чату
        # Это используется в дальнейшем, чтобы рассылать новые сообщения
        self.clients.add_client(self)

        await self.ws.send(json.dumps({'method': 'userChats', 'data': self.chats}))

    async def handler_auth(self, data):
        username = data['username']
        password = get_hash(data['password'] + password_salt)
        user = self.db.cur.execute('SELECT * FROM users WHERE name = ?', [username]).fetchall()

        if not user:
            # Регистрируем пользователя
            self.db.cur.execute(
                'INSERT INTO users(name, password) VALUES (?, ?)',
                [username, password]
            )
            self.db.con.commit()
        elif password != user[0][2]:
            # Неверный пароль
            await self.ws.send(json.dumps({'method': 'auth', 'success': False}))
            return

        user = self.db.cur.execute('SELECT id, name FROM users WHERE name = ?', [username]).fetchall()[0]

        self.id = user[0]
        self.name = user[1]

        await self.ws.send(json.dumps({
            'method': 'auth',
            'success': True,
            'data': {'id': self.id, 'name': self.name}
        }))
        # Сразу отправляем список чатов пользователя
        await self.handler_userChats()

    async def handler_createChat(self, data):
        if not data['name']:
            await self.ws.send(json.dumps({'method': 'createChat', 'success': False,
                                           'text': 'Не указано название чата'}))
            return

        invite_code = random_invite_code(6)

        # Создание чата
        self.db.cur.execute(
            'INSERT INTO chats(name, invite_code, admin_id) VALUES (?, ?, ?)',
            [data['name'], invite_code, self.id]
        )
        chat_id = self.db.cur.lastrowid

        # Добавление пользователя в список участников
        self.db.cur.execute(
            'INSERT INTO user_chats(user_id, chat_id) VALUES (?, ?)',
            [self.id, chat_id]
        )
        self.db.con.commit()

        await self.handler_userChats()

        await self.send_system_message(
            chat_id,
            f'Чат успешно создан! ID: {chat_id}, Инвайт-код: {invite_code}'
        )

        await self.send_system_message(chat_id, f'Пользователь {self.name} вошёл в чат')
        await self.ws.send(json.dumps({'method': 'createChat', 'success': True}))
        await self.handler_getMessages(int(chat_id))

    async def handler_joinChat(self, invite_code: str):
        # Ищем чат с таким инвайт-кодом
        chat = self.db.cur.execute('SELECT * FROM chats WHERE invite_code=?', [invite_code.upper()]).fetchall()

        if not chat:
            await self.ws.send(json.dumps({
                'method': 'joinChat', 'success': False, 'text': 'Несуществующий инвайт-код'
            }))
            return

        try:
            # Добавляем пользователя в список участников
            self.db.cur.execute(
                'INSERT INTO user_chats(user_id, chat_id) VALUES (?, ?)',
                [self.id, chat[0][0]]
            )
            self.db.con.commit()
            await self.handler_userChats()
            await self.send_system_message(chat[0][0], f'Пользователь {self.name} вошёл в чат')
            await self.ws.send(json.dumps({'method': 'joinChat', 'success': True}))
            await self.handler_getMessages(int(chat[0][0]))
        except:
            await self.ws.send(json.dumps({
                'method': 'joinChat', 'success': False, 'text': 'Вы уже в этом чате'
            }))

    async def send_system_message(self, chat_id, message):
        # Метод для быстрой отправки сообщения от имени системы
        await self.handler_send({'msg': message, 'chat_id': chat_id}, user_id=1, username='System')

    async def handler_send(self, data, user_id=None, username=None):
        # Обработка нового сообщения
        chat_id = int(data['chat_id'])
        msg = data['msg']

        self.db.cur.execute(
            'INSERT INTO messages(chat_id, user_id, message) VALUES (?, ?, ?)',
            [chat_id, user_id if user_id else self.id, msg]
        )
        data = self.db.cur.execute(
            'SELECT id, chat_id, created_at, message FROM messages WHERE id=?',
            [self.db.cur.lastrowid]
        ).fetchall()[0]
        self.db.con.commit()

        # Отправляем всем участникам чата уведомление о новом сообщении
        await self.clients.sync_message(
            chat_id,
            [data[0], data[1], data[2], username if username else self.name, data[3]]
        )

    async def handler_getMessages(self, chat_id: int):
        # Получение списка всех сообщений
        data = self.db.cur.execute('''
            SELECT m.id, m.chat_id, m.created_at, u.name, message FROM messages m 
            INNER JOIN users u on m.user_id = u.id
            WHERE m.chat_id=? ORDER BY m.created_at
        ''', [chat_id]).fetchall()
        await self.ws.send(json.dumps({'method': 'messages', 'data': data}))