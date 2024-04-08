import asyncio
from typing import List

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.loader import bot, logger
from filters.auth import AuthorizedOnly
from keyboards.inline.menu import callbackKeywords, menu_keyboard, check_keyboard
from models import Meal, MealType, Menu, User
from models.meal import default_img_src
from services.meal import get_meal, list_meal_types, list_menu_meals
from services.menu import get_menu_for_today, get_menu_for_tomorrow
from services.messages import messageBuilder
from services.order import create_order, insert_order_meal_relations

router = Router(name="menu_choose")


order_img_src = "https://www.barony-biggar.co.uk/wp-content/uploads/2015/12/MENU.png"


class OrderForm(StatesGroup):
    user_id = State()
    choosen_meals = State()
    total_price = State()
    types = State()
    menu_name = State()
    current_type_id = State()
    has_next_type = State()
    has_previos_type = State()


async def process_order_create(menu: Menu, message: Message, session: AsyncSession, state: FSMContext, user: User) -> None:
    types = await list_meal_types(session)

    data = await state.update_data(
        user_id=user.id,
        menu_name=menu.name,
        total_price=0.0,
        choosen_meals=[],
        types=[{"id": type.id, "name": type.name} for type in types],
        has_next_type=len(types) > 1,
        has_previous_type=False,
        current_type_id=0
    )

    # TODO: change photo to some nice menu photo
    await message.answer_photo(
        photo=order_img_src,
        caption=messageBuilder.choose_menu(menu.name),
        reply_markup=await menu_keyboard(session, menu.id, data)
    )


@router.message(F.text == "🕒 Обрати меню на сьогодні", AuthorizedOnly())
async def choose_for_today(message: Message, session: AsyncSession, state: FSMContext, user: User) -> None:
    menu: Menu = await get_menu_for_today(session)

    if menu is None:
        return await message.answer(
            messageBuilder.menu_not_exist(),
        )

    await process_order_create(menu, message, session, state, user)


@router.message(F.text == "🕥 Обрати меню на завтра", AuthorizedOnly())
async def choose_for_today(message: Message, session: AsyncSession, state: FSMContext, user: User) -> None:
    menu: Menu = await get_menu_for_tomorrow(session)

    if menu is None:
        return await message.answer(
            messageBuilder.menu_not_exist(),
        )
    
    await process_order_create(menu, message, session, state, user)


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "next"))
async def process_next(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "next_"):]
    menu_id = int(callback_data)
    data = await state.get_data()

    current_type_id = data["current_type_id"] + 1

    await state.update_data(current_type_id=current_type_id)
    await state.update_data(has_next_type=len(data["types"]) > current_type_id + 1)
    data = await state.update_data(has_previous_type=current_type_id > 0)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, data)
    )


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "previous"))
async def process_previous(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "previous_"):]
    menu_id = int(callback_data)
    data = await state.get_data()

    current_type_id = data["current_type_id"] - 1

    await state.update_data(current_type_id=current_type_id)
    await state.update_data(has_next_type=len(data["types"]) > current_type_id + 1)
    data = await state.update_data(has_previous_type=current_type_id > 0)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, data)
    )


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "cancel"))
async def process_cancel(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "add"))
async def process_add(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "add_"):]
    meal_id, menu_id = map(int, callback_data.split('_'))
    meal: Meal = await get_meal(session, meal_id)

    data = await state.get_data()

    updated_meals: List = data["choosen_meals"]
    updated_meals.append({"id": meal_id})

    total_price = float(data["total_price"]) + meal.price

    updated_data = await state.update_data(choosen_meals=updated_meals, total_price=total_price)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, updated_data)
    )


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "remove"))
async def process_remove(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "remove_"):]
    meal_id, menu_id = map(int, callback_data.split('_'))
    meal: Meal = await get_meal(session, meal_id)

    data = await state.get_data()

    total_price = float(data["total_price"]) - meal.price

    updated_data = await state.update_data(
        choosen_meals=[meal for meal in data["choosen_meals"] if meal["id"] != meal_id],
        total_price=total_price
    )

    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, updated_data)
    )


@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "data"))
async def process_data(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "data_"):]
    meal_id, menu_id = map(int, callback_data.split('_'))

    meal: Meal = await get_meal(session, meal_id)
    data = await state.get_data()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=meal.img_url,
            caption=messageBuilder.choose_menu_meal(
                data["menu_name"], meal.name, meal.price)
        ),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, data)
    )

@router.callback_query(F.data.startswith(callbackKeywords.choose_menu + "check"))
async def process_check(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.choose_menu + "check_"):]
    menu_id = int(callback_data)

    data = await state.get_data()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=order_img_src,
            caption=messageBuilder.choose_menu_check(data["total_price"])
        ),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await check_keyboard(session, menu_id, data)
    )

@router.callback_query(F.data.startswith(callbackKeywords.check + "back"))
async def process_check_back(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.check + "back_"):]
    menu_id = int(callback_data)

    data = await state.get_data()

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=order_img_src,
            caption=messageBuilder.choose_menu(data["menu_name"])
        ),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_keyboard(session, menu_id, data)
    )

@router.callback_query(F.data.startswith(callbackKeywords.check + "remove"))
async def process_check_remove(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.check + "remove_"):]
    meal_id, menu_id = map(int, callback_data.split('_'))
    meal: Meal = await get_meal(session, meal_id)

    data = await state.get_data()

    total_price = float(data["total_price"]) - meal.price

    updated_data = await state.update_data(
        choosen_meals=[meal for meal in data["choosen_meals"] if meal["id"] != meal_id],
        total_price=total_price
    )

    await bot.edit_message_caption(
        caption=messageBuilder.choose_menu_check(updated_data["total_price"]),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await check_keyboard(session, menu_id, updated_data)
    )

@router.callback_query(F.data.startswith(callbackKeywords.check + "confirm"))
async def process_check_confirm(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.check + "confirm_"):]
    menu_id = int(callback_data)

    data = await state.get_data()

    if len(data["choosen_meals"]) == 0:
        return await callback_query.answer("Ви не обрали жодної страви!")

    new_order = await create_order(data, menu_id, session)
    await insert_order_meal_relations(new_order.id, data["choosen_meals"], session)

    await bot.edit_message_caption(
        caption=messageBuilder.check_confirm(new_order.id, new_order.total_price),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id
    )