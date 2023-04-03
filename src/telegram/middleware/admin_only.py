from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from setup import admins


class AdminOnly(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        if event.from_user.id in admins:
            return await handler(event, data)