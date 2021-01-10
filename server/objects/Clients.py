from objects.User import User
import json


class Clients:
    def __init__(self):
        self.clients = []
        self.chats_online = {}

    def add_client(self, user: User):
        for chat in user.chats:
            x = self.chats_online.get(chat['id'], [])
            if user not in x:
                x.append(user)
                self.chats_online[chat['id']] = x

    def remove_client(self, user: User):
        for id in self.chats_online.keys():
            chat_users = self.chats_online[id]
            if user in chat_users:
                chat_users.remove(user)
                self.chats_online[id] = chat_users

    async def sync_message(self, chat_id, data):
        # Рассылка нового сообщения всем пользователям в чате
        for user in self.chats_online[int(chat_id)]:
            await user.ws.send(json.dumps({'method': 'newMessage', 'data': data}))