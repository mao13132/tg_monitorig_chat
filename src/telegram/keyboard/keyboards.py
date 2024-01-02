from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Call_admin:

    def admin(self):
        self._admin = CallbackData('adm', 'type', 'number', 'id')

        return self._admin


class Admin_keyb(Call_admin):
    def start_keyb(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔑 Ключевые слова', callback_data='words'))

        self._start_key.add(InlineKeyboardButton(text=f'🙋‍ Каналы', callback_data='channels'))

        return self._start_key

    def stop(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'➕ Добавить слово', callback_data='add_word'))

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_pamel'))

        return core_keyb

    def back_add_words(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='words'))

        return core_keyb
