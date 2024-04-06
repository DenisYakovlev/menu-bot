from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
import json

from filters.manager import ManagerOnly
from services.messages import messageBuilder
from services.menu import get_menu, add_meal_to_menu, remove_meal_from_menu
from models.user import User
from models.menu import Menu
from keyboards.inline.menu_settings import menu_edit_keyboard, menu_meal_edit_keyboard, menu_meal_add_keyboard, callbackKeywords
from core import logger
from core.loader import bot


router = Router(name="menu_edit")


@router.message(F.text == "🖊 Редагувати меню", ManagerOnly())
async def menu_update(message: Message, session: AsyncSession) -> None:
    """
        Init Inline keyboard for menu editing
    """
    await message.answer(
        messageBuilder.menu_edit(),
        reply_markup=await menu_edit_keyboard(session)
    )


@router.callback_query(F.data.startswith(callbackKeywords.menu_edit))
async def menu_edit(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Menu level
        List all menus in db
    """
    menu_id = int(callback_query.data[len(callbackKeywords.menu_edit):])
    menu: Menu = await get_menu(session, menu_id)

    await bot.edit_message_text(
        text=messageBuilder.menu_edit_meals(menu.name),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_meal_edit_keyboard(session, menu_id)
    )

@router.callback_query(F.data.startswith(callbackKeywords.menu_meal_edit + "delete_"))
async def menu_edit_delete(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Meals level
        Remove meal from chosen menu
    """
    callback_data = callback_query.data[len(callbackKeywords.menu_meal_edit + "delete_"):]
    menu_id, meal_id = map(int, callback_data.split('_'))

    menu: Menu = await get_menu(session, menu_id)
    await remove_meal_from_menu(session, menu_id, meal_id)

    await bot.edit_message_text(
        text=messageBuilder.menu_edit_meals(menu.name),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_meal_edit_keyboard(session, menu_id)
    )

@router.callback_query(F.data.startswith(callbackKeywords.menu_meal_edit + "back"))
async def menu_meal_edit_back(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Meals level
        Go back to all menu list like in menu_edit handler
    """
    await bot.edit_message_text(
        text=messageBuilder.menu_edit(),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_edit_keyboard(session)
    )

@router.callback_query(F.data.startswith(callbackKeywords.menu_meal_edit + "new"))
async def menu_meal_edit_new(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Add Meals level
        Open all meals that can be added to menu
    """
    menu_id = int(callback_query.data[len(callbackKeywords.menu_meal_edit + "new_"):])

    await bot.edit_message_text(
        text=messageBuilder.add_meal_to_menu(),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_meal_add_keyboard(session, menu_id)
    )

@router.callback_query(F.data.startswith(callbackKeywords.menu_meal_add + "back_"))
async def menu_meal_add_back(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Add Meals level
        Go back to menu meals level
    """
    menu_id = int(callback_query.data[len(callbackKeywords.menu_meal_add + "back_"):])
    menu: Menu = await get_menu(session, menu_id)

    await bot.edit_message_text(
        text=messageBuilder.menu_edit_meals(menu.name),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_meal_edit_keyboard(session, menu_id)
    )

@router.callback_query(F.data.startswith(callbackKeywords.menu_meal_add + "data_"))
async def menu_meal_add(callback_query: CallbackQuery, session: AsyncSession) -> None:
    """
        Add meals level
        Add chosen meal to chosen menu
    """
    callback_data = callback_query.data[len(callbackKeywords.menu_meal_add + "data_"):]
    menu_id, meal_id = map(int, callback_data.split('_'))

    await add_meal_to_menu(session, menu_id, meal_id)

    await bot.edit_message_text(
        text=messageBuilder.add_meal_to_menu(),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await menu_meal_add_keyboard(session, menu_id)
    )