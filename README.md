# Проект PyQT для Яндекс.Лицея
## Идея проекта
Асинхронный чат с клиентской и серверной частью, которые общаются по WebSocket

### Для каких задач создан
Общение в реальном времени по сети

## Функционал
- Авторизация и регистрация
- Создание чатов
- Система инвайт-кодов
- Вход в существующие чаты по инвайт-кодам
- Отправка и получение сообщений в реальном времени

## Реализация
Клиентская и серверная части написаны на классах. Для общения между сервисами на бекенде используется асинхронная библиотека [`websockets`](https://github.com/aaugustin/websockets), а на фронтенде класс [`QtWebSockets`](https://doc.qt.io/qt-5/qtwebsockets-index.html).<br/>
Хранение данных происходит в базе данных SQLite. Есть система регистрации с проверкой правильности ввода пароля. Все пароли, хранящиеся в базе данных, хешируются алгоритмом `sha256` с добавлением криптографической соли.<br/><br/>
Когда приходит новое сообщение, бекенд рассылает уведомление всем пользователям в чате. Если связь с бекендом пропадает, то на фронтенде есть обработчики, которые направляют пользователя на экран повторной авторизации.<br/><br/>
Также на фронтенде есть возможность поменять адрес сервера. Это позволяет подключаться не только к серверу в локальной сети, но и к внешним серверам, в том числе по `wss` протоколу

### Используемые технологии
- Python 3.8
- PyQT 5
- WebSockets
- SQLite
- AsyncIO

## Как запускать
1. Скачайте зависимости `pip3 install requirements.txt`
2. Запустите `server/run.py`
3. Запустите `client/run_client.py`

## Автор проекта
[Ильсур Гильмутдинов](https://ilsur.dev/?ref=github&project=classbattle) &#60;me@ilsur.dev&#62;<br/>
