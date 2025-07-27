from pyrogram import Client

from core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH


def get_pyrogram_client():
    client = Client('reply4u', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    return client
