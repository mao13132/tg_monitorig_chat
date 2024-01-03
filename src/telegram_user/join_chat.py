# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime

from src.telegram.logic._logger import logger_msg
from src.telegram_user.is_flood import is_flood


class JoinChat:
    def __init__(self, app):
        """@developer_telegrams"""

        self.app = app

    async def join_to_chat(self, name_chat):
        """@developer_telegrams"""
        try:

            response = await self.app.join_chat(name_chat)

        except Exception as es:

            if 'FLOOD' in str(es):
                res = await is_flood(es)

                return res

            if 'USER_ALREADY_PARTICIPANT' in str(es):

                return True

            if 'INVITE_REQUEST_SENT' in str(es):
                print(f'Заявку на вступление успешно отправил "{name_chat}"')

                return False

            if 'Username not found' in str(es):
                print(f'Данный ресурс не доступен "{name_chat}"')

                return False

            if 'INVITE_HASH_EXPIRED' in str(es):
                print(f'У ссылка вышел срок действия. Удалите из настройке "{name_chat}"')

                return False

            if 'USERNAME_INVALID' in str(es) or 'USERNAME_NOT_OCCUPIED' in str(es):
                logger_msg(f'Чата "{name_chat}" не существует. Удалите из настроек')

                return False

            msg = f'Не могу подписаться на канал "{name_chat}" "{es}"'

            logger_msg(msg)

            return False

        return True
