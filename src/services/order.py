from typing import Dict, List

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis import build_key, cached, clear_cache
from core import logger
from models import Meal, Order, order_meal_relation


async def create_order(data: Dict, menu_id: int, session: AsyncSession) -> Order:
    new_order: Order = Order(
        user_id=data["user_id"],
        menu_id=menu_id,
        total_price=data["total_price"]
    )

    session.add(new_order)

    await session.commit()
    await session.refresh(new_order)

    await clear_cache(list_user_orders, new_order.user_id)

    return new_order


async def insert_order_meal_relations(order_id: int, meals: List, session: AsyncSession) -> None:
    query = insert(order_meal_relation).values(
        [{"order_id": order_id, "meal_id": meal["id"]} for meal in meals]
    )

    await session.execute(query)
    await session.commit()


@cached(key_builder=lambda order_id, session: build_key(order_id))
async def list_order_meals(order_id: int, session: AsyncSession) -> list[Meal]:
    query = select(Meal).join(Order.meals).filter(Order.id == order_id)

    result = await session.execute(query)
    meals: List[Meal] = result.scalars().all()

    return meals


@cached(key_builder=lambda user_id, session: build_key(user_id))
async def list_user_orders(user_id: int, session: AsyncSession) -> List[Order]:
    query = select(Order).filter_by(user_id=user_id)
    result = await session.execute(query)

    orders: List[Order] = result.scalars().all()
    return orders


@cached(key_builder=lambda session: build_key())
async def list_unpaid_orders(session: AsyncSession) -> List[Order]:
    """
    List only orders with is_paid = False
    """
    query = select(Order).filter_by(is_paid=False)
    result = await session.execute(query)

    orders: List[Order] = result.scalars().all()
    return orders


@cached(key_builder=lambda order_id, session: build_key(order_id))
async def get_order(order_id: int, session: AsyncSession) -> Order:
    order: Order = await session.get(Order, order_id)

    return order


async def set_order_paid(order_id: int, session: AsyncSession) -> Order:
    order: Order = await session.get(Order, order_id)

    order.is_paid = True

    await session.commit()
    await session.refresh(order)

    await clear_cache(list_unpaid_orders)
    await clear_cache(get_order, order_id)

    return order
