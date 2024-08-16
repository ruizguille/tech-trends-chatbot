import os
import json
import asyncio
from app.db import get_redis, get_all_chats
from app.config import settings

async def export_chats(export_dir=settings.EXPORT_DIR):
    print('Exporting chats to JSON')
    file_path = os.path.join(export_dir, 'chats.json')
    async with get_redis() as rdb:
        chats = await get_all_chats(rdb)
        with open(file_path, 'w') as file:
            json.dump(chats, file, indent=2)
    print(f'{len(chats)} chats exported')

def main():
    asyncio.run(export_chats())


if __name__ == '__main__':
    main()