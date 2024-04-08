from typing import Dict, List, Tuple

from sqlalchemy import select, not_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.meal import Meal, default_img_src
from models.menu import Menu
from models.meal_menu_relation import meal_menu_relation
from models.meal_type import MealType
from core import logger
from cache.redis import cached, build_key, clear_cache


@cached(key_builder=lambda session: build_key())
async def list_meal_types(session: AsyncSession) -> List[MealType]:
    """
    List all types of meal
    """
    query = select(MealType)

    result = await session.execute(query)
    types: List[MealType] = result.scalars().all()

    return types

async def list_menu_meals(session: AsyncSession, menu_id: int) -> List[Meal]:
    query = select(Meal).join(Menu.meals).filter(Menu.id == menu_id)

    result = await session.execute(query)
    meals: List[Meal] = result.scalars().all()

    return meals


async def list_menu_meal_by_type(session: AsyncSession, menu_id: int, type_id: int) -> List[Meal]:
    """
    List meals for specific meal types from MealType table
    """
    query = select(Meal).join(Menu.meals).filter(Menu.id == menu_id, Meal.type_id == type_id)

    result = await session.execute(query)
    meals: List[Meal] = result.scalars().all()

    return meals

async def list_unused_meals(session: AsyncSession, menu_id: int)-> List[Meal]:
    """
    Retrieve all meals that are not in given menu
    """
    query = select(Meal, MealType).join(Meal.meal_type).filter(not_(Meal.menus.any(Menu.id == menu_id)))
    result = await session.execute(query)

    meals = result.scalars().all()
    return meals


async def create_meal(data: Dict, session: AsyncSession) -> Meal:
    """
    Create new meal from form data
    """
    new_meal = Meal(
        name=data["name"],
        price=float(data["price"]),
        img_url=default_img_src if data["img_url"] == "default" else data["img_url"] ,
        type_id=int(data["type_id"])
    )

    session.add(new_meal)

    await session.commit()
    await session.refresh(new_meal)

    await clear_cache(list_meals)

    return new_meal


@cached(key_builder=lambda session, meal_id: build_key(meal_id))
async def get_meal(session: AsyncSession, meal_id: int) -> Meal:
    """
    Return meal from given id
    """
    meal: Meal = await session.get(Meal, meal_id)
    return meal


async def get_meal_from_ids(session: AsyncSession, id_list: int) -> List[Meal]:
    query = select(Meal).filter(Meal.id.in_(id_list))
    result = await session.execute(query)

    meals: List[Meal] = result.scalars().all()
    return meals


@cached(key_builder=lambda session: build_key())
async def list_meals(session: AsyncSession) -> List[Meal]:
    query = select(Meal)
    result = await session.execute(query)

    meals: List[Meal] = result.scalars().all()
    return meals


async def get_meal_type(session: AsyncSession, meal_id: int) -> MealType:
    query = select(MealType).join(Meal.meal_type).filter(Meal.id == meal_id)
    result = await session.execute(query)

    type: MealType = result.scalar_one()
    return type