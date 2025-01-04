import keyboards
from aiogram.types import CallbackQuery
from aiogram import Router, types, F
from services import UserSettingsService

router = Router()

@router.message(F.text == "Tilni o'zgartirish⚙️")
async def changeLanguageUz(message: types.Message):
    try:
        await message.answer("Tilni tanlang.", reply_markup=keyboards.languages)
    except:
        await message.answer("Nimadir xato ketdi, /start - Qaytadan urunib ko'ring", reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text == "Изменить язык⚙️")
async def changeLanguageUz(message: types.Message):
    try:
        await message.answer("Выберите язык.", reply_markup=keyboards.languages)
    except:
        await message.answer("Что-то пошло не так, /start – попробуйте еще раз.", reply_markup=types.ReplyKeyboardRemove())


@router.callback_query(lambda c: c.data == "uz" or c.data == "ru")
async def change_language(callback_query: CallbackQuery):
    try:
        lang = callback_query.data.replace(' ', '')
        user_id = callback_query.from_user.id
        await UserSettingsService.change(user_id, 1 if lang == "uz" else 2)
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        if userSettings.LanguageId == 1:
            await callback_query.message.delete()
            await callback_query.message.answer("Til o'zgardi🇺🇿", reply_markup=keyboards.main_menu_uz)
        elif userSettings.LanguageId == 2:
            await callback_query.message.delete()
            await callback_query.message.answer("Язык изменился🇷🇺", reply_markup=keyboards.main_menu_ru)
    except:
        await callback_query.message.answer("Nimadir xato ketdi, Qaytadan urunib ko'ring")