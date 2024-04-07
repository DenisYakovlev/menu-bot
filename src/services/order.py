from typing import Dict, List
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Order, order_meal_relation, Meal
from core import logger


async def create_order(data: Dict, menu_id: int, session: AsyncSession) -> Order:
    new_order: Order = Order(
        user_id=data["user_id"],
        menu_id=menu_id,
        total_price=data["total_price"]
    )

    session.add(new_order)

    await session.commit()
    await session.refresh(new_order)

    return new_order

async def insert_order_meal_relations(order_id: int, meals: List, session: AsyncSession) -> None:
    query = insert(order_meal_relation).values(
        [{"order_id": order_id, "meal_id": meal["id"]} for meal in meals]
    )

    await session.execute(query)
    await session.commit()

async def list_order_meals(order_id: int, session: AsyncSession) -> list[Meal]:
    query = select(Meal).join(Order.meals).filter(Order.id == order_id)

    result = await session.execute(query)
    meals: List[Meal] = result.scalars().all()

    return meals

async def list_user_orders(user_id: int, session: AsyncSession) -> List[Order]:
    query = select(Order).filter_by(user_id=user_id)
    result = await session.execute(query)

    orders: List[Order] = result.scalars().all()
    return orders


async def list_unpaid_orders(session: AsyncSession) -> List[Order]:
    query = select(Order).filter_by(is_paid=False)
    result = await session.execute(query)

    orders: List[Order] = result.scalars().all()
    return orders

async def get_order(order_id: int, session: AsyncSession) -> Order:
    order: Order = await session.get(Order, order_id)

    return order

async def set_order_paid(order_id: int, session: AsyncSession) -> Order:
    order: Order = await get_order(order_id, session)

    order.is_paid = True

    await session.commit()
    await session.refresh(order)

    return order

