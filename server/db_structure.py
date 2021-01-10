QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,
    name text NOT NULL,
    password text NOT NULL
);
CREATE UNIQUE INDEX users_id_uindex on users (id);
CREATE UNIQUE INDEX users_name_uindex on users (name);

INSERT INTO users(name, password) VALUES ('System', 'password');

CREATE TABLE IF NOT EXISTS chats (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,
    name text NOT NULL,
    invite_code text NOT NULL,
    created_at timestamp default current_timestamp,
    admin_id integer NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX chats_id_uindex on chats (id);
CREATE UNIQUE INDEX chats_invite_code_uindex on chats (invite_code);

CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,
    chat_id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL,
    created_at timestamp default current_timestamp,
    FOREIGN KEY (chat_id) REFERENCES chats (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX messages_chatId_index on messages (chat_id);
CREATE UNIQUE INDEX messages_id_uindex on messages (id);

CREATE TABLE IF NOT EXISTS user_chats (
    user_id integer NOT NULL,
    chat_id integer NOT NULL,
    entry_date timestamp default current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (chat_id) REFERENCES chats (id)
);

CREATE INDEX user_chats_userId_index on user_chats (user_id);
CREATE INDEX user_chats_chatId_index on user_chats (chat_id);
CREATE UNIQUE INDEX user_chats_index on user_chats (user_id, chat_id);
"""