import datetime
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"monitoring (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_chat TEXT, id_msg TEXT, date DATETIME, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table monitoring {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"words (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"word TEXT, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table words {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"channels (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"link TEXT, id_chanel TEXT, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table channels {es}')

    def add_message(self, id_chat, id_msg):

        result = self.cursor.execute(f"SELECT * FROM monitoring WHERE id_chat='{id_chat}' AND id_msg='{id_msg}'")

        response = result.fetchall()

        if response == []:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO monitoring ('id_chat',"
                                "'id_msg', "
                                "'date') VALUES (?,?,?)",
                                (id_chat, id_msg,
                                 now_date,))

            self.conn.commit()
            return True

        return False

    def exist_message(self, id_chat, id_msg):
        try:
            result = self.cursor.execute(f"SELECT * FROM monitoring WHERE id_chat='{id_chat}' AND id_msg='{id_msg}'")

            response = result.fetchall()

        except Exception as es:
            print(f'Ошибка при проверки существования записи из TG канала "{es}"')
            return False

        if response == []:
            return False

        return True

    def update_id_channel(self, id_pk, id_channel):

        self.cursor.execute(f"UPDATE channels SET id_chanel = '{id_channel}' WHERE id_pk='{id_pk}'")

        self.conn.commit()

        return True

    def get_channels(self):

        result = self.cursor.execute(f"SELECT * FROM channels")

        response = result.fetchall()

        return response

    def get_word(self):

        result = self.cursor.execute(f"SELECT * FROM words")

        response = result.fetchall()

        return response

    def add_words(self, word):

        result = self.cursor.execute(f"SELECT * FROM words WHERE word='{word}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute("INSERT OR IGNORE INTO words ('word') VALUES (?)",
                                (word,))

            self.conn.commit()

            return True

        return False

    def add_channels(self, link):

        result = self.cursor.execute(f"SELECT * FROM channels WHERE link='{link}'")

        response = result.fetchall()

        if response == []:
            self.cursor.execute("INSERT OR IGNORE INTO channels ('link') VALUES (?)",
                                (link,))

            self.conn.commit()

            return True

        return False

    def del_word(self, id_pk):

        try:
            result = self.cursor.execute(f"DELETE FROM words WHERE id_pk = '{id_pk}'")

            self.conn.commit()

            x = result.fetchall()

        except Exception as es:
            msg = (f'Ошибка SQL del_word: {es}')

            print(msg)

            return False

        return True

    def del_channel(self, id_pk):

        try:
            result = self.cursor.execute(f"DELETE FROM channels WHERE id_pk = '{id_pk}'")

            self.conn.commit()

            x = result.fetchall()

        except Exception as es:
            msg = (f'Ошибка SQL del_channel: {es}')

            print(msg)

            return False

        return True

    def close(self):
        # Закрытие соединения
        self.conn.close()

        print('Отключился от SQL BD')
