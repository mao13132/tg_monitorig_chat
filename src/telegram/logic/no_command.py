# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram.types import Message


async def no_command(message: Message):

    await message.bot.send_message(message.chat.id, message.text)
