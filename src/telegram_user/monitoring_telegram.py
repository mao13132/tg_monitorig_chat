import asyncio
import time

from pyrogram import Client

from settings import *

from datetime import datetime

from src.telegram.logic._logger import logger_msg
from src.telegram_user.is_flood import is_flood
from src.telegram_user.join_chat import JoinChat
from src.telegram_user.replace_name_channel import replace_name_channel


class MonitoringTelegram:
    def __init__(self, BotDB, bot_start):
        """@developer_telegrams"""

        self.BotDB = BotDB

        self.path = sessions_path + f'/{API_ID}'

        self.bot_start = bot_start

    async def start_tg(self):

        print(f'{datetime.now().strftime("%H:%M:%S")} Инициализирую вход в аккаунт {API_ID}')

        try:
            self.app = Client(self.path, API_ID, API_HASH)

            await self.app.start()

        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка при авторизации ({API_ID}) "{es}"')

            return False

        return True

    async def join_to_chat(self, chat):
        """@developer_telegrams"""
        try:
            name_chat = chat.replace('https://t.me/', '')

            response = await self.app.join_chat(name_chat)
        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка join_chat ()  "{es}"')

            return False

        return True

    async def formated_msg(self, message, target_keyb, chat_id):
        """@developer_telegrams"""

        try:
            first_name = message.from_user.first_name
        except:
            first_name = 'Не указан'

        try:

            last_name = message.from_user.last_name if message.from_user.last_name else 'Не указан'
        except:
            last_name = 'Не указан'

        try:
            username = f'https://t.me/{message.from_user.username}'
        except:
            username = 'Не указан'

        try:
            id_msg = message.from_user.id if message.from_user.id else 'Не указан'
        except:
            id_msg = 'Не указан'

        message_text = message.text if message.text else message.caption

        msg = f'Monitoring Bot: найден ключевик "{target_keyb}"\n\n' \
              f'Чат: {chat_id}\n\n' \
              f'Автор сообщения: {first_name} {last_name}\n\n' \
              f'Дата сообщения {message.date}\n\n' \
              f'ID: {id_msg} профиль: {username}\n\n' \
              f'Ссылка на сообщение {message.link}\n\n' \
              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
              f'Тест сообщения:\n"{message_text}"\n'

        return msg

    # async def in_black(self, lower_msg):
    #     for black in BLACKS:
    #         if black.lower() in lower_msg:
    #             return True
    #
    #     return False

    async def check_msg_to_keybs(self, message):
        """@developer_telegrams"""

        keyboards_list = self.BotDB.get_word()

        text_message = message.text if message.text else message.caption

        if text_message is None:
            return False

        for keyb_row in keyboards_list:

            keyb = keyb_row[1]

            try:
                lower_keyb = keyb.lower()

                lower_msg = text_message.lower()

            except:

                lower_keyb = keyb

                lower_msg = ''

            if lower_keyb in lower_msg:
                return keyb

        return False

    async def _send_admin(self, msg):
        """@developer_telegrams"""

        send_ = await self.bot_start.bot.send_message(CHAT_FROM_SEND, msg, disable_web_page_preview=True)

        return True

    async def send_admin(self, message, target_keyb, chat_id):
        """@developer_telegrams"""

        msg = await self.formated_msg(message, target_keyb, chat_id)

        resp = await self._send_admin(msg)

        return False

    async def start_monitoring_chat(self, chat_id, link_chat, id_pk_chat):

        for _try in range(3):

            try:
                count = 0

                async for message in self.app.get_chat_history(chat_id):
                    count += 1

                    if count > COUNT_SCRAP:
                        msg = f'Обработал сообщения в {link_chat}. Останавливаюсь по лимиту в {COUNT_SCRAP}'

                        print(msg)

                        return True

                    exist_msg = self.BotDB.exist_message(chat_id, message.id)

                    if exist_msg:
                        print(f'Обработал все новые сообщения "{link_chat}"')

                        return True

                    valid_msg = await self.check_msg_to_keybs(message)

                    sql_res = self.BotDB.add_message(chat_id, message.id)

                    if not sql_res:
                        print(
                            f'{datetime.now().strftime("%H:%M:%S")} Все новые сообщения из чата {link_chat} обработаны')

                        return True

                    if valid_msg:
                        resp_admin = await self.send_admin(message, valid_msg, chat_id)

            except Exception as es:
                if 'PEER_ID_INVALID' in str(es):
                    ### незнакомый чат

                    if _try == 0:
                        name_chat = replace_name_channel(link_chat)

                        if not name_chat:
                            return False

                        res_join = await JoinChat(self.app).join_to_chat(name_chat)

                        if not res_join:
                            return False

                        continue

                    logger_msg(f'Выгнали из чата или незнакомый чат')

                    self.BotDB.update_id_channel(id_pk_chat, '')

                    return False

                if 'CHANNEL_INVALID' in str(es):
                    logger_msg(f'{datetime.now().strftime("%H:%M:%S")} Вы не подписаны на канал "{chat_id}" '
                               f'или бота исключили')

                    return False

                logger_msg(
                    f'{datetime.now().strftime("%H:%M:%S")} Ошибка при получении сообщений из "{chat_id}" "{es}"')

                return False

            print(f'Обработку {link_chat} закончил')

            return True

    async def get_id_chat(self, name_link):
        """@developer_telegrams"""

        name_chat = replace_name_channel(name_link)

        if not name_chat:
            return False

        try:

            res_join = await JoinChat(self.app).join_to_chat(name_chat)

            if not res_join:
                return False

            res_chat = await self.app.get_chat(name_chat)

            id_chat = res_chat.id

        except Exception as es:
            if 'FLOOD' in str(es):
                res = await is_flood(es)

                return res

            logger_msg(f'--- Проблема с ссылкой на чат: "{name_link}" "{es}"')

            time.sleep(ITER_SLEEP)

            return False

        return id_chat

    async def start_monitoring(self):
        """@developer_telegrams ТВХ"""

        channels_list_sql = self.BotDB.get_channels()

        for count, channel_row in enumerate(channels_list_sql):
            """Итерация списка с каналами"""

            id_pk_chat = channel_row[0]

            link_chat = channel_row[1]

            id_chat = channel_row[2]

            if id_chat is None or not id_chat:
                id_chat = await self.get_id_chat(link_chat)

                if not id_chat:
                     continue

                self.BotDB.update_id_channel(id_pk_chat, id_chat)

            if id_chat == 'FLOOD':
                return 'FLOOD'

            if not id_chat:
                continue

            print(f'\n{datetime.now().strftime("%H:%M:%S")} #{count + 1} Обрабатываю сообщения из чата: {link_chat}')

            resp_monit = await self.start_monitoring_chat(id_chat, link_chat, id_pk_chat)

            if resp_monit == "FLOOD":
                return "FLOOD"

            time.sleep(ITER_SLEEP)

        print(f'{datetime.now().strftime("%H:%M:%S")} Закончил мониторинг списка чатов')

        return True
