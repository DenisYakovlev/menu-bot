from typing import List
from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from core.exceptions import UserUpdateError
from cache.redis import build_key, cached, clear_cache


async def register_user(user: types.User, session: AsyncSession) -> User:
    """
    Register user from start command
    """
    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )

    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    await clear_cache(user_exists, new_user.id)

    return new_user

@cached(key_builder=lambda user_id, session: build_key(user_id))
async def user_exists(user_id: int, session: AsyncSession) -> bool:
    """
    Check if user exists in db
    """
    query = select(User.id).filter_by(id=user_id).limit(1)

    result = await session.execute(query)
    user = result.scalar_one_or_none()

    return bool(user)

@cached(key_builder=lambda user_id, session: build_key(user_id))
async def fetch_user(user_id: int, session: AsyncSession) -> User:
    """
    Fetch user from db
    """
    query = select(User).filter_by(id=user_id).limit(1)

    result = await session.execute(query)
    user = result.scalar_one_or_none()

    return user


async def update_user_from_contact(user: User, contact: types.Contact, session: AsyncSession) -> User:
    """
    Update user from provided contact
    """
    if not User:
        raise UserUpdateError()
    
    user.phone_number = contact.phone_number
    user.first_name = contact.first_name
    user.last_name = contact.last_name

    await session.commit()
    await session.refresh(user)

    await clear_cache(fetch_user, user.id)

    return user


async def change_user_status(user: User, session: AsyncSession) -> User:
    """
    Change is_manager value
    """
    if not User:
        raise UserUpdateError()
    
    user.is_manager = not user.is_manager

    await session.commit()
    await session.refresh(user)

    await clear_cache(fetch_user, user.id)

    return user
