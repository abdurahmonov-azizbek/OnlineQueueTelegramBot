import asyncio
import config
import keyboards
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import *
from handlers.change_language_handler import router as ChangeLangRouter
from handlers.feedback_handler import router as FeedbackRouter
from services import UserSettingsService

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(ChangeLangRouter)
dp.include_router(FeedbackRouter)

@dp.message(Command("start"))
async def welcome(message: Message):
    userSettings = await UserSettingsService.get_by_telegram_id(message.from_user.id)
    if not userSettings:
        await UserSettingsService.change(message.from_user.id, 1)
        await message.answer("Assalomu alaykum, botga xush kelibsiz", reply_markup=keyboards.main_menu_uz)    
    
    elif userSettings.LanguageId == 1:
        await message.answer("Assalomu alaykum, botga xush kelibsiz", reply_markup=keyboards.main_menu_uz)
    elif userSettings.LanguageId == 2:
        await message.answer("Привет и добро пожаловать в бот", reply_markup=keyboards.main_menu_ru)

async def main():
    print("Starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 