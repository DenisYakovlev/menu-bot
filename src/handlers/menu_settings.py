from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import date

from filters.manager import ManagerOnly
from keyboards.reply.menu_settings import menu_settings_keyboard, entity_create_keyboard
from models.user import User
from services.messages import messageBuilder
from services.meal import create_meal
from services.menu import validate_menu_date, create_menu
from keyboards.inline.menu_settings import meal_type_keyboard
from models.meal import Meal
from core.loader import bot

router = Router(name="menu_settings")

class MenuForm(StatesGroup):
    name = State()
    date = State()

class MealForm(StatesGroup):
    name = State()
    price = State()
    img_url = State()
    type_id = State()


@router.message(F.text == "⚙️ Налаштування меню", ManagerOnly())
async def menu_settings(message: Message) -> None:
    await message.answer(
        messageBuilder.menu_settings(),
        reply_markup=menu_settings_keyboard()
    )



@router.message(F.text == "❌ Відмінити", ManagerOnly())
async def cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state:
        await state.clear()
    
    await menu_settings(message)

# menu create

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
        messageBuilder.menu_create_success(name=data["name"], date=data["date"]),
        reply_markup=menu_settings_keyboard()
    )

# menu update    

@router.message(F.text == "🖊 Редагувати меню", ManagerOnly())
async def menu_update(message: Message, user: User, session: AsyncSession) -> None:
    await message.answer("mock")

# meal create

@router.message(F.text == "🛠 Створити страву", ManagerOnly())
async def meal_create(message: Message, state: FSMContext) -> None:
    await state.set_state(MealForm.name)
    await message.answer(messageBuilder.meal_create(), reply_markup=entity_create_keyboard())


@router.message(MealForm.name, F.text, ManagerOnly())
async def process_meal_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(MealForm.price)

    await message.answer(messageBuilder.meal_create_price())

@router.message(MealForm.price, F.text.func(lambda x: int(x) <= 0), ManagerOnly())
async def process_meal_invalid_price(message: Message, state: FSMContext) -> None:
    await message.answer(messageBuilder.meal_create_price_error())

@router.message(MealForm.price, F.text.func(lambda x: int(x) > 0), ManagerOnly())
async def process_meal_price(message: Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    await state.set_state(MealForm.img_url)

    await message.answer(messageBuilder.meal_create_img_url())


@router.message(
    MealForm.img_url, 
    F.text.regexp(r'^(?!https?://(?:www\\.)?[ a-zA-Z0-9./]+)'), 
    ManagerOnly()
)
async def process_meal_invalid_img_url(message: Message) -> None:
    await message.answer(messageBuilder.meal_create_img_url_error())

@router.message(
    MealForm.img_url, 
    F.text.regexp(r'https?://(?:www\\.)?[ a-zA-Z0-9./]+'), 
    ManagerOnly()
)
async def process_meal_img_url(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(img_url=message.text)
    await state.set_state(MealForm.type_id)

    await message.answer(
        messageBuilder.meal_create_type_id(), 
        reply_markup=await meal_type_keyboard(session)
    )


@router.callback_query(F.data.startswith("meal_type_"))
async def test(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    meal_type_id = callback_query.data[len("meal_type_"):]
    data = await state.update_data(type_id=meal_type_id)
    await state.clear()

    new_meal: Meal = await create_meal(data, session)

    await bot.send_photo(
        chat_id=callback_query.from_user.id,
        caption=messageBuilder.meal_create_success(new_meal.name, new_meal.price),
        photo=new_meal.img_url,
        reply_markup=menu_settings_keyboard(),
    )


@router.message(F.text == "🖊 Редагувати страву", ManagerOnly())
async def meal_update(message: Message, user: User, session: AsyncSession) -> None:
    await message.answer("mock")


@router.message(F.text.func(lambda x: int(x) > 0))
async def test(message: Message) -> None:
    await message.answer("ok")

 