from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.telegram.handlers.users import start
from src.telegram.logic.devision_msg import division_message
from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States


async def back_admin(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_call(call)

    await start(call.message)

    return True


async def words(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    id_user = call.message.chat.id

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().stop()

    stop_word_list = BotDB.get_word()

    if stop_word_list == []:
        _msg = '⛔️ Список слов пуст'

        print(f'{id_user}: {_msg}')

        await Sendler_msg.send_msg_call(call, _msg, keyb)

        return False

    _msg = '<b>Список ключевых слов:</b>\n\n'

    _msg += f'\n'.join(f'{word[1]} - Удалить /del_{word[0]}' for word in stop_word_list)

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)


async def add_word(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    id_user = call.message.chat.id

    await Sendler_msg.log_client_call(call)

    _msg = f'<b>Укажите список стоп слов</b>\n\n' \
           f'Можете указывать сразу несколько слов\n' \
           f'разделять пробелом, запятой или переносим строки'

    keyb = Admin_keyb().back_add_words()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_stop_word.set()

    async with state.proxy() as data:
        data['admin'] = id_user


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(words, text='words', state='*')

    dp.register_callback_query_handler(back_admin, text_contains='admin_pamel', state='*')

    dp.register_callback_query_handler(add_word, text='add_word', state='*')
