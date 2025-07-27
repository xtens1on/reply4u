import os

from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

SETTINGS_PATH = BASE_DIR / 'settings.json'
JSON_USER_STORE_PATH = BASE_DIR / 'users.json'

load_dotenv()

USER_STORAGE_TYPE = os.getenv('USER_STORAGE_TYPE')

DB = {
    'DRIVER': os.getenv('DB_DRIVER'),
    'USERNAME': os.getenv('DB_USERNAME'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'HOST': os.getenv('DB_HOST'),
    'PORT': os.getenv('DB_PORT'),
    'NAME': os.getenv('DB_NAME')
}

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

LLM_PROVIDER = os.getenv('LLM_PROVIDER')

OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

RESPONSE_DELAY = int(os.getenv('RESPONSE_DELAY'))  # in seconds

FRONTEND_HOSTS = os.getenv('FRONTEND_HOSTS').split(',')
