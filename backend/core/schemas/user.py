import json

from typing import List
from pyrogram.types import User as TelegramUser, Chat

from pydantic import BaseModel, Json


class UserInDBSchema(BaseModel):
    telegram_id: int
    active: bool
    description: str | None = None
    chat_history: Json[List] | None = None

    def update(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
        return self

    def update_context(self, messages: list[str], role: str = 'user'):
        message_objects = [{
            'content': message,
            'role': role,
        } for message in messages]
        if not self.chat_history:
            self.chat_history = message_objects
            return
        self.chat_history += message_objects

    def db_dump(self, exclude_none: bool = False, exclude: set[str] = None):
        data = self.model_dump(exclude_none=exclude_none, exclude=exclude)
        if data.get('chat_history'):
            data['chat_history'] = json.dumps(data['chat_history'])
        return data


class CreateUserSchema(BaseModel):
    telegram_id: int
    active: bool = False
    description: str | None = None


class PatchUserSchema(BaseModel):
    active: bool | None = None
    description: str | None = None


class TelegramUserSchema(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    title: str | None = None

    def merge_telegram(self, user: TelegramUser | Chat):
        self.telegram_id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        if isinstance(user, Chat):
            self.title = user.title


class UserSchema(UserInDBSchema, TelegramUserSchema):

    def db_dump(self, exclude_none: bool = False, exclude: set[str] = None):
        db_fields = set(UserInDBSchema.model_fields.keys())
        exclude_fields = set(TelegramUserSchema.model_fields.keys()) - db_fields
        return super().db_dump(exclude=exclude_fields)

    @property
    def shortcuts(self):
        return {
            'username': self.username,
            'description': self.description,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title,
            'telegram_id': self.telegram_id,
        }
