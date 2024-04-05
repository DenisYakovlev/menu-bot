from typing import Any, Optional
from aiogram.filters import BaseFilter

from models.user import User


class AuthorizedOnly(BaseFilter):
    async def __call__(self, *args, **kwargs) -> bool:
        # Get user data from kwargs
        user: User = kwargs.get("user")

        # Allow only active users
        # User object is obtained from auth middleware
        return user and user.is_active