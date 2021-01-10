from database import Database
from objects.User import User
from objects.Clients import Clients
import logging
import asyncio
import websockets

IP = 'localhost'
PORT = 4180

FORMAT = '[%(asctime)-15s] [%(levelname)s] - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.info('Запуск сервера...')

db = Database('database.sqlite')
db.setup()

clients = Clients()


async def ws_handler(websocket, path):
    user = User(websocket, db, clients)
    await user.listen_messages()


start_server = websockets.serve(ws_handler, IP, PORT)

logging.info(f'Запущен WebSocket сервер. {IP}:{PORT}')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()