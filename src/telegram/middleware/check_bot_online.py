from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from config import admins
from setup import get_status
from src.database.tables import User

blocked_users = set()


def block_user(user_id: int) -> bool:
    user = User.get(user_id=user_id)
    user.banned = True
    user.save()
    blocked_users.add(user_id)


def unblock_user(user_id: int) -> bool:
    try:
        blocked_users.remove(user_id)
        user = User.get(user_id=user_id)
        user.banned = True
        user.save()
        return True
    except KeyError:
        return False


class CheckOnline(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        if event.from_user.id in blocked_users:
            "User is blocked"
            pass
        elif get_status() or event.from_user.id in admins:
            return await handler(event, data)
