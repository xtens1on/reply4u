import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from core.schemas.user import UserSchema
from core.services.user import UserService
from core.services.llm import LLMService

from core.config import RESPONSE_DELAY


class OnMessage:
    queue: dict[int, list[Message]] = {}

    @classmethod
    async def on_message(cls, client: Client, message: Message):
        telegram_id = message.from_user.id
        me = await client.get_me()
        if telegram_id == me.id:
            return
        user = await UserService.get_or_create_user(telegram_id=telegram_id)
        if not user.active:
            return
        user.merge_telegram(message.from_user)
        await cls.queue_message(message)
        await cls.respond(client, message, user)

    @classmethod
    async def queue_message(cls, message: Message):
        if cls.queue.get(message.from_user.id):
            cls.queue[message.from_user.id].append(message)
            return
        cls.queue[message.from_user.id] = [message]

    @classmethod
    async def respond(cls, client: Client, message: Message, user: UserSchema):

        await asyncio.sleep(RESPONSE_DELAY)
        last_message = cls.queue[user.telegram_id][-1]
        if last_message.id != message.id:
            return

        text_messages = [message.text for message in cls.queue[user.telegram_id]]
        del cls.queue[user.telegram_id]
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        response = await LLMService.generate_response(user, text_messages)
        await client.send_chat_action(message.chat.id, ChatAction.CANCEL)
        await message.reply_text(response)
