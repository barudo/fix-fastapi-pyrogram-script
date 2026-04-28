from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from telegram_util import TelegramClient

tg_client = TelegramClient('mbark444')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await tg_client.start()
    try:
        yield
    finally:
        await tg_client.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/test_telegram")
async def test_telegram():
    return await tg_client.get_chat_history(-1001621981937, limit=10)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
