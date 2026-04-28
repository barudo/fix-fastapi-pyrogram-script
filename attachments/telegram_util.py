from utils.utils_general import *
from pyrogram import Client as PyrogramClient
from pyrogram.handlers import MessageHandler

class TelegramClient:
    def __init__(self, username):
        self.client = PyrogramClient(
            name=username,
            api_id=os.getenv('TELEGRAM_API_ID'),
            api_hash=os.getenv('TELEGRAM_API_HASH')
        )
        self.client.add_handler(MessageHandler(self.handle_message))

    async def start(self):
        await self.client.start()

    async def get_chat_history(self, chat_id: str | int, limit = 10):
        messages = self.client.get_chat_history(chat_id, limit=limit)
        result = list([msg async for msg in messages])
        return [r.text for r in result]

    async def handle_message(self, client, message):
        # THIS NEVER GETS CALLED!
        print(message)

