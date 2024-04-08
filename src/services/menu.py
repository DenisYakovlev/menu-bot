from datetime import date, datetime, timedelta
from typing import Dict, List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Menu, Meal, meal_menu_relation
from core.exceptions import InvalidDateError
from core import logger
from cache.redis import cached, build_key, clear_cache
from .meal import list_menu_meals, list_unused_meals



def convert_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()

@cached(key_builder=lambda date, session: build_key(date))
async def get_menu_by_date(date: date, session: AsyncSession) -> Menu:
    query = select(Menu).filter_by(date=date).limit(1)
    result = await session.execute(query)

    menu: Menu = result.scalar_one_or_none()
    return menu

async def get_menu_for_today(session: AsyncSession) -> Menu:
    today = date.today()
    return await get_menu_by_date(today, session)

async def get_menu_for_tomorrow(session: AsyncSession) -> Menu:
    tomorrow = date.today() + timedelta(days=1)
    return await get_menu_by_date(tomorrow, session)


async def validate_menu_date(date_str: str, session: AsyncSession) -> None:
    """
    New menu date validation
    """
    try:
        converted_date = convert_date(date_str)
    except:
        raise InvalidDateError("Такої дати не існує...")

    if converted_date < date.today():
        raise InvalidDateError("Потрібно вести дату, яка не раніше ніж сьогодні")
    
    query = select(Menu).filter_by(date=converted_date).limit(1)
    result = await session.execute(query)

    menu = result.scalar_one_or_none()

    if menu:
        raise InvalidDateError("Вже існує меню на цю дату")
    

async def create_menu(data: Dict, session: AsyncSession) -> Menu:
    """
    Create menu from form data
    """
    converted_date = convert_date(data["date"])

    new_menu = Menu(
        name=data["name"],
        date=converted_date
    )

    session.add(new_menu)

    await session.commit()
    await session.refresh(new_menu)

    await clear_cache(list_menus)
    await clear_cache(get_menu_by_date, new_menu.date)

    return new_menu

@cached(key_builder=lambda session: build_key())
async def list_menus(session: AsyncSession) -> Menu:
    current_date = date.today()

    query = select(Menu).filter(Menu.date >= current_date)
    result = await session.execute(query)
    menus: List[Menu] = result.scalars().all()

    return menus


@cached(key_builder=lambda session, menu_id: build_key(menu_id))
async def get_menu(session: AsyncSession, menu_id: int) -> Menu:
    menu: Menu = await session.get(Menu, menu_id)

    return menu


async def add_meal_to_menu(session: AsyncSession, menu_id: int, meal_id: int) -> None:
    query = insert(meal_menu_relation).values(menu_id=menu_id, meal_id=meal_id)
    await session.execute(query)

    await session.commit()

    menu = await get_menu(session, menu_id)

    await clear_cache(list_menu_meals, menu_id)
    await clear_cache(list_unused_meals, menu_id)
    await clear_cache(get_menu_by_date, menu.date)


async def remove_meal_from_menu(session: AsyncSession, menu_id: int, meal_id: int) -> None:
    query = delete(meal_menu_relation).filter_by(menu_id=menu_id, meal_id=meal_id)
    result = await session.execute(query)

    await session.commit()
    
    menu = await get_menu(session, menu_id)

    await clear_cache(list_menu_meals, menu_id)
    await clear_cache(list_unused_meals, menu_id)
    await clear_cache(get_menu_by_date, menu.date)
