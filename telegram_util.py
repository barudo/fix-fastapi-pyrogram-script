import logging
import os

from pyrogram import Client as PyrogramClient
from pyrogram.handlers import MessageHandler


logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, username):
        self.username = username
        self.client = None

    async def start(self):
        if self.client and self.client.is_connected:
            return

        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        session_string = os.getenv('TELEGRAM_SESSION_STRING')

        if not api_id or not api_hash:
            raise RuntimeError(
                'TELEGRAM_API_ID and TELEGRAM_API_HASH must be set before starting Telegram'
            )

        self.client = PyrogramClient(
            name=self.username,
            api_id=int(api_id),
            api_hash=api_hash,
            session_string=session_string
        )
        self.client.add_handler(MessageHandler(self.handle_message))
        await self.client.start()
        logger.info('Telegram client started')

    async def stop(self):
        if self.client and self.client.is_connected:
            await self.client.stop()
            logger.info('Telegram client stopped')

    async def get_chat_history(self, chat_id: str | int, limit=10):
        if not self.client or not self.client.is_connected:
            raise RuntimeError('Telegram client is not started')

        messages = self.client.get_chat_history(chat_id, limit=limit)
        result = list([msg async for msg in messages])
        return [r.text for r in result]

    async def handle_message(self, client, message):
        logger.info('New Telegram message: %s', message)
        print(message)
