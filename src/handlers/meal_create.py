from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, File
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters.manager import ManagerOnly
from services.messages import messageBuilder
from keyboards.inline.menu_settings import meal_type_keyboard, callbackKeywords
from keyboards.reply.menu_settings import entity_create_keyboard, menu_settings_keyboard
from models.meal import Meal
from services.meal import create_meal
from core.loader import bot, logger, settings


router = Router(name="meal_create")

class MealForm(StatesGroup):
    name = State()
    price = State()
    img_url = State()
    type_id = State()


@router.message(F.text == "🛠 Створити страву", ManagerOnly())
async def meal_create(message: Message, state: FSMContext) -> None:
    await state.set_state(MealForm.name)
    await message.answer(messageBuilder.meal_create(), reply_markup=entity_create_keyboard())


@router.message(MealForm.name, F.text, ManagerOnly())
async def process_meal_name(message: Message, state: FSMContext) -> None:
    """
    Name processing
    """
    await state.update_data(name=message.text)
    await state.set_state(MealForm.price)

    await message.answer(messageBuilder.meal_create_price())

@router.message(MealForm.price, F.text.func(lambda x: int(x) <= 0), ManagerOnly())
async def process_meal_invalid_price(message: Message, state: FSMContext) -> None:
    await message.answer(messageBuilder.meal_create_price_error())

@router.message(MealForm.price, F.text.func(lambda x: int(x) > 0), ManagerOnly())
async def process_meal_price(message: Message, state: FSMContext) -> None:
    """
    Price processing
    """
    await state.update_data(price=message.text)
    await state.set_state(MealForm.img_url)

    await message.answer(messageBuilder.meal_create_img_url())


@router.message(MealForm.img_url, F.text =="-", ManagerOnly())
async def process_meal_img_url_default(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """
    Img url processing
    """
    await state.update_data(img_url="default")
    await state.set_state(MealForm.type_id)

    await message.answer(
        messageBuilder.meal_create_type_id(), 
        reply_markup=await meal_type_keyboard(session)
    )

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


@router.callback_query(F.data.startswith(callbackKeywords.meal_type))
async def process_meal_type(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """
    Type processing
    """
    meal_type_id = callback_query.data[len(callbackKeywords.meal_type):]
    data = await state.update_data(type_id=meal_type_id)
    await state.clear()

    new_meal: Meal = await create_meal(data, session)

    await bot.send_photo(
        chat_id=callback_query.from_user.id,
        caption=messageBuilder.meal_create_success(new_meal.name, new_meal.price),
        photo=new_meal.img_url,
        reply_markup=menu_settings_keyboard(),
    )
