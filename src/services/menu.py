from datetime import date, datetime
from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Menu
from core.exceptions import InvalidDateError


def convert_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()


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

    return new_menu
