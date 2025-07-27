from fastapi.routing import APIRouter

from core.services.telegram import TelegramService

router = APIRouter(prefix='/telegram')


@router.get('/list')
async def telegram_users_list(limit: int = 0, q: str = '', only_active: bool = None):
    users = await TelegramService.list_users(limit=limit, query=q, only_active=only_active)
    return users


@router.get('/me')
async def get_my_account():
    user = await TelegramService.get_my_account()
    return user
