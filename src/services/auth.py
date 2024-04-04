from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def register_user(user: types.User, session: AsyncSession) -> bool:
    """
        Register user from start command
        Return True if user successfully created
        Return False if user is already exists
    """

    if await user_exists(user.id, session):
        return False

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )

    session.add(new_user)

    await session.commit()
    return True


async def user_exists(user_id: int, session: AsyncSession) -> bool:
    """
        Check if user exists in db
    """
    query = select(User.id).filter_by(id=user_id).limit(1)

    result = await session.execute(query)
    user = result.scalar_one_or_none()

    return bool(user)