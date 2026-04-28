import asyncio
import os

from pyrogram import Client


async def main():
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    if not api_id or not api_hash:
        raise RuntimeError('Set TELEGRAM_API_ID and TELEGRAM_API_HASH first')

    async with Client(
        name='session_generator',
        api_id=int(api_id),
        api_hash=api_hash,
        in_memory=True
    ) as client:
        session_string = await client.export_session_string()
        print(session_string)


if __name__ == '__main__':
    asyncio.run(main())
