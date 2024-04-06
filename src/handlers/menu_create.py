from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters.manager import ManagerOnly
from services.messages import messageBuilder
from keyboards.reply.menu_settings import entity_create_keyboard, menu_settings_keyboard
from services.menu import create_menu, validate_menu_date


router = Router(name="menu_create")


class MenuForm(StatesGroup):
    name = State()
    date = State()


@router.message(F.text == "🛠 Створити меню", ManagerOnly())
async def menu_create(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuForm.date)
    await message.answer(messageBuilder.menu_create(), reply_markup=entity_create_keyboard())


@router.message(MenuForm.date, F.text.regexp(r'(?!\d{4}-\d{2}-\d{2}$)'), ManagerOnly())
async def process_menu_date_invalid(message: Message) -> None:
    await message.answer(messageBuilder.menu_create_date_error())


@router.message(MenuForm.date, F.text.regexp(r'\d{4}-\d{2}-\d{2}'), ManagerOnly())
async def process_menu_date(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await validate_menu_date(message.text, session)
    await state.update_data(date=message.text)
    await state.set_state(MenuForm.name)

    await message.answer(messageBuilder.menu_create_name())


@router.message(MenuForm.name, F.text, ManagerOnly())
async def process_menu_name(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.update_data(name=message.text)
    await state.clear()

    await create_menu(data, session)
    await message.answer(
        messageBuilder.menu_create_success(
            name=data["name"], date=data["date"]),
        reply_markup=menu_settings_keyboard()
    )
