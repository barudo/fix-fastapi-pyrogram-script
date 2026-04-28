import uvicorn
from fastapi import FastAPI
from telegram_util import TelegramClient

app = FastAPI()
tg_client = TelegramClient('mbark444')

@app.get("/test_telegram")
async def test_telegram():
    return await tg_client.get_chat_history(-1001621981937, limit=10)

@app.on_event('startup')
async def startup():
    await tg_client.start()
    # tg_client.client.add_handler(tg_client.handle_message)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)



