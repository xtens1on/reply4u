from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.client import get_pyrogram_client
from core.services.telegram import TelegramService
from core.config import FRONTEND_HOSTS

from api.telegram.routes import router as telegram_router
from api.app.routes import router as core_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    client = get_pyrogram_client()
    await client.start()
    TelegramService.set_client(client)
    yield


app = FastAPI(title='reply4u', lifespan=lifespan)
app.include_router(telegram_router)
app.include_router(core_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
