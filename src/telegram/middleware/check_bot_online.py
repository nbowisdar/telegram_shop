from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from config import admins
from setup import get_status


class CheckOnline(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        if get_status() or event.from_user.id in admins:
            return await handler(event, data)
