from datetime import datetime

from pyrogram.handlers import MessageHandler

from core.client import get_pyrogram_client

from core.handlers.message import OnMessage


def main():
    client = get_pyrogram_client()
    client.add_handler(MessageHandler(OnMessage.on_message))
    print(f"STARTED | {datetime.now()}")
    client.run()


if __name__ == "__main__":
    main()
