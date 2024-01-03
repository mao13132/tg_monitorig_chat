import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram', '.env')

sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram_user', 'sessions')

load_dotenv(dotenv_path)

ADMIN = ['1422194909', '49892631']

CHAT_FROM_SEND = -1002135915102

TOKEN = os.getenv('TOKEN')

START_MESSAGE = 'Админ меню'

LOGO = r'src/telegram/media/logo.jpg'

API_ID = os.getenv('API_ID')

API_HASH = os.getenv('API_HASH')

ITER_SLEEP = 30

COUNT_SCRAP = 15
