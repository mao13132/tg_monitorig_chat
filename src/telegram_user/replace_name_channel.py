# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram.logic._logger import logger_msg


def replace_name_channel(link):
    try:
        if "+" in link or 'joinchat' in link or '@' in link:
            link = link.strip()

            return link

        if 'https://t.me/' in link:
            name_chat = link.replace('https://t.me/', '')

        elif 'http://t.me/' in link:
            name_chat = link.replace('http://t.me/', '')

        else:

            return link

    except Exception as es:

        msg = f'Не смог вытащить имя канала из ссылки "{link}" "{es}"'

        logger_msg(msg)

        return False

    return name_chat
