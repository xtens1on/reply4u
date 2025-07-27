from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Chat, Dialog

from core.schemas.user import TelegramUserSchema, UserSchema

from core.services.user import UserService


class TelegramService:
    client: Client | None = None
    user_service = UserService

    @classmethod
    def set_client(cls, client: Client):
        if not client.is_connected:
            raise ValueError('Client should be started before being passed to service.')
        cls.client = client

    @classmethod
    async def list_users(cls,
                         limit: int = 0,
                         query: str = '',
                         only_active: bool = False,
                         ) -> list[TelegramUserSchema]:
        if only_active:
            return await cls._list_active_users(limit=limit, query=query)

        users = []
        async for dialog in cls.client.get_dialogs():
            if not await cls._is_matching_dialog(dialog, query):
                continue
            user = await cls._get_user_from_dialog(dialog)
            users.append(user)
            if limit != 0 and len(users) == limit:
                break
        merged_users = await cls._merge_db_users(users)
        return merged_users

    @classmethod
    async def _list_active_users(cls, limit: int = 0, query: str = '') -> list[UserSchema]:
        users = await cls.user_service.list_users(only_active=True)
        matching_users = []
        for user in users:
            chat = await cls.client.get_chat(user.telegram_id)
            if not await cls._chat_name_contains(chat, query):
                continue
            user.merge_telegram(chat)
            matching_users.append(user)
            if limit != 0 and len(matching_users) == limit:
                break
        return matching_users

    @classmethod
    async def _is_matching_dialog(cls, dialog: Dialog, query: str) -> bool:
        if dialog.chat.type not in (ChatType.BOT, ChatType.PRIVATE, ChatType.SUPERGROUP):
            return False
        if not await cls._chat_name_contains(dialog.chat, query):
            return False
        return True

    @classmethod
    async def _chat_name_contains(cls, chat: Chat, query: str) -> bool:
        query = query.lower().strip()
        username_contains = None
        title_contains = None
        first_name_contains = None
        last_name_contains = None
        id_contains = query in str(chat.id)
        if chat.username:
            username_contains = query in chat.username.lower()
        if chat.title:
            title_contains = query in chat.title.lower()
        if chat.first_name:
            first_name_contains = query in chat.first_name.lower()
        if chat.last_name:
            last_name_contains = query in chat.last_name.lower()
        return any(
            (
                username_contains,
                title_contains,
                id_contains,
                first_name_contains,
                last_name_contains,
            )
        )

    @classmethod
    async def _get_user_from_dialog(cls, dialog: Dialog) -> TelegramUserSchema:
        user = TelegramUserSchema(
            telegram_id=dialog.chat.id,
            username=dialog.chat.username,
            first_name=dialog.chat.first_name,
            last_name=dialog.chat.last_name,
            title=dialog.chat.title,
        )
        return user

    @classmethod
    async def _merge_db_users(
            cls,
            telegram_users: list[TelegramUserSchema],
    ) -> list[TelegramUserSchema]:

        users = await cls.user_service.list_users()
        mapped_users = {user.telegram_id: user for user in users}

        merged_users = []
        for telegram_user in telegram_users:
            user = mapped_users.get(telegram_user.telegram_id)
            if not user:
                merged_users.append(telegram_user)
                continue
            user.update(**telegram_user.model_dump())
            merged_users.append(user)
        return merged_users

    @classmethod
    async def get_my_account(cls) -> TelegramUserSchema:
        account = await cls.client.get_me()
        return TelegramUserSchema(
            telegram_id=account.id,
            username=account.username,
            first_name=account.first_name,
            last_name=account.last_name,
        )
