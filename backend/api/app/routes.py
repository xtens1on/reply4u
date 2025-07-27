from fastapi import status
from fastapi.routing import APIRouter

from core.schemas.settings import UpdateAppSettingsSchema
from core.schemas.user import PatchUserSchema
from core.services.llm import LLMService
from core.services.user import UserService
from core.services.settings import SettingsService


router = APIRouter(prefix='')


@router.post('/user/{telegram_id}', status_code=status.HTTP_201_CREATED)
async def update_or_create_user(telegram_id: int, data: PatchUserSchema):
    user = await UserService.update_or_create_user(telegram_id, data)
    return user


@router.delete('/user/{telegram_id}/history', status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_chat_history(telegram_id: int):
    await UserService.clear_user_chat_history(telegram_id)


@router.get('/settings')
async def get_app_settings():
    settings = await SettingsService.get_settings()
    return settings


@router.patch('/settings')
async def update_app_settings(settings: UpdateAppSettingsSchema):
    await SettingsService.update(settings)


@router.get('/models')
async def models_list(q: str = '', limit: int = 10):
    models = await LLMService.models_list(query=q, limit=limit)
    return models
