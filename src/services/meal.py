from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.meal import Meal
from models.meal_type import MealType


async def list_meal_types(session: AsyncSession) -> List[MealType]:
    """
        List all types of meal
    """
    query = select(MealType)

    result = await session.execute(query)
    types: List[MealType] = result.scalars().all()

    return types


async def create_meal(data: Dict, session: AsyncSession) -> Meal:
    """
        Create new meal from form data
    """
    new_meal = Meal(
        name=data["name"],
        price=float(data["price"]),
        img_url=data["img_url"],
        type_id=int(data["type_id"])
    )

    session.add(new_meal)

    await session.commit()
    await session.refresh(new_meal)

    return new_meal