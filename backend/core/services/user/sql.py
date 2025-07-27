from sqlalchemy import select, Select, update

from core.db.session import get_sessionmaker

from core.models.user import User
from core.schemas.user import UserSchema, UserInDBSchema, PatchUserSchema, CreateUserSchema
from core.services.settings import SettingsService

from .base import BaseUserService


class UserServiceSQL(BaseUserService):
    Session = get_sessionmaker()

    @classmethod
    async def list_users(cls, limit: int = None, only_active: bool = False) -> list[UserSchema]:
        async with cls.Session.begin() as session:
            query = select(User)
            query = await cls._apply_filters(query, limit=limit, only_active=only_active)
            users = await session.scalars(query)
            return [await cls._serialize(user) for user in users]

    @classmethod
    async def _apply_filters(cls, query: Select, limit: int = None, only_active: bool = False):
        if only_active:
            query = query.where(User.active == True)  # noqa: E712
        if limit:
            query = query.limit(limit)
        return query

    @classmethod
    async def get_user(cls, telegram_id: int) -> UserSchema | None:
        async with cls.Session.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            user = await session.scalar(query)
            if not user:
                return None
            serialized_user = await cls._serialize(user)
            return serialized_user

    @classmethod
    async def _serialize(cls, user: User) -> UserSchema:
        return UserSchema(
            telegram_id=user.telegram_id,
            description=user.description,
            chat_history=user.chat_history,
            active=user.active,
        )

    @classmethod
    async def get_or_create_user(cls, telegram_id: int) -> UserSchema:
        user = await cls.get_user(telegram_id)
        if not user:
            data = CreateUserSchema(telegram_id=telegram_id)
            user = await cls.create_user(data)
        return user

    @classmethod
    async def create_user(cls, data: CreateUserSchema) -> UserSchema:
        if not data.active:
            settings = await SettingsService.get_settings()
            data.active = settings.users_active_by_default
        async with cls.Session.begin() as session:
            user = User(**data.model_dump())
            session.add(user)
            await session.commit()
        user = await cls.get_user(data.telegram_id)
        return user

    @classmethod
    async def update_or_create_user(cls, telegram_id: int, data: PatchUserSchema) -> UserInDBSchema:
        user = await cls.get_user(telegram_id)
        if user:
            user.update(**data.model_dump())
            await cls.save(user)
            return user
        full_data = CreateUserSchema(telegram_id=telegram_id, **data.model_dump())
        user = await cls.create_user(full_data)
        return user

    @classmethod
    async def save(cls, user: UserInDBSchema):
        user_data = user.db_dump(exclude_none=True)

        async with cls.Session.begin() as session:
            query = update(User).where(User.telegram_id == user.telegram_id).values(**user_data)
            await session.execute(query)

    @classmethod
    async def clear_user_chat_history(cls, telegram_id: int):
        async with cls.Session.begin() as session:
            query = update(User).values(chat_history=None).where(User.telegram_id == telegram_id)
            await session.execute(query)
