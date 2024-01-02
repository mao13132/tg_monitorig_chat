import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram', '.env')

load_dotenv(dotenv_path)

ADMIN = ['1422194909']

TOKEN = os.getenv('TOKEN')

START_MESSAGE = 'Админ меню'

LOGO = r'src/telegram/media/logo.jpg'
