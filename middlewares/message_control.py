import asyncio
from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config_data.config


class MessageController(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        await asyncio.sleep(float(config_data.config.DELAY))
        print('Awaiting for some seconds...')
        return await handler(event, data)