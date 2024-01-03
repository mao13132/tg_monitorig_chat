# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
from datetime import datetime

from src.telegram.logic._logger import logger_msg


async def is_flood(es):
    try:
        seconds = es.value // 60
    except:
        seconds = 1

    logger_msg(f'\n --- {(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} '
               f'Телеграм заблокировал аккаунт на {seconds} минут(ы) за частоту действий. Встаю в ожидание')

    await asyncio.sleep(seconds * 61)

    if seconds == 0:
        return 'FLOOD'

    return False
