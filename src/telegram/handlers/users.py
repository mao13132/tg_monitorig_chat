from aiogram.types import Message

from aiogram import Dispatcher, types

from settings import START_MESSAGE, ADMIN, LOGO
from src.telegram.logic.no_command import no_command
from src.telegram.sendler.sendler import Sendler_msg


async def start(message: Message):
    id_user = message.chat.id

    if str(id_user) in ADMIN:
        keyb = None

        await Sendler_msg().sendler_photo_message(message, LOGO, START_MESSAGE, keyb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
    # dp.register_message_handler(no_command, text_contains='', content_types=[types.ContentType.ANY])
