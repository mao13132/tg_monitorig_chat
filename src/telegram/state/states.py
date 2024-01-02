from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from settings import LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logic.devision_msg import division_message
from src.telegram.logic.scrap_stop_words import scrap_stop_words
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


class States(StatesGroup):
    add_stop_word = State()

    add_channels = State()


async def add_stop_word(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    _stop_word_list = message.text

    stop_word_list = await scrap_stop_words(_stop_word_list)

    if stop_word_list == []:
        keyb = Admin_keyb().back_add_words()

        error = f'⚠️ Вы не верно указали ключевое слово(а). Попробуйте ещё раз'

        await Sendler_msg.send_msg_message(message, error, keyb)

        return False

    [BotDB.add_words(stop_word) for stop_word in stop_word_list]

    _msg = f'✅ <b>Стоп слова успешно добавлены:</b>' \
           f'\n\n{" ".join(f"<b>{word}</b>" for word in stop_word_list)}'

    keyb = Admin_keyb().back_add_words()

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    await state.finish()


async def add_channels(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    _channels_list = message.text

    channels_list = await scrap_stop_words(_channels_list)

    if channels_list == []:
        keyb = Admin_keyb().back_add_channels()

        error = f'⚠️ Вы не верно указали канал(ы). Попробуйте ещё раз'

        await Sendler_msg.send_msg_message(message, error, keyb)

        return False

    [BotDB.add_channels(channel) for channel in channels_list]

    _msg = f'✅ <b>Канал(ы) успешно добавлены:</b>' \
           f'\n\n{" ".join(f"<b>{word}</b>" for word in channels_list)}'

    keyb = Admin_keyb().back_add_channels()

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(add_stop_word, state=States.add_stop_word)

    dp.register_message_handler(add_channels, state=States.add_channels)
