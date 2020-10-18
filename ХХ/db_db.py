import sqlite3
def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('C:/XX/db.sqlite3') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS user news_artiles1')

    c.execute('''
        CREATE TABLE IF NOT EXISTS news_artiles1 (
            id          INTEGER PRIMARY KEY, 
            title        TEXT NOT NULL,
            anons     TEXT NOT NULL,
            full_text  TEXT NOT NULL,
            img     TEXT NOT NULL,
            date    TEXT NOT NULL 
            )
''')

    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_message(conn,title: str, anons: str, full_text: str, img: str, date: str):
    c = conn.cursor()
    c.execute('INSERT INTO news_artiles1 (title, anons, full_text, img, date) VALUES (?, ?, ?, ?, ?)', (title, anons, full_text, img, date))
    conn.commit()


# @ensure_connection
# def count_messages(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ? LIMIT 1', (user_id, ))
#     (res, ) = c.fetchone()
#     return res
#
#
# @ensure_connection
# def list_messages(conn, user_id: int, limit: int = 10):
#     c = conn.cursor()
#     c.execute('SELECT user_id, name, surname FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
#     return c.fetchall()
