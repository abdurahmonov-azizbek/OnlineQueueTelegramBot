from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import *
from services import UserSettingsService, FeedbackService
from functions import *
import keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

class CreateFeedback(StatesGroup):
    PhoneNumber = State()
    WasRude = State()
    SentToPrivateClinic = State()
    ServiceQuality = State()
    DoctorName = State()

@router.message(lambda c: c.text == "Оценка⭐️" or c.text == "Baxolash⭐️")
async def ask_phone(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        feedback = await FeedbackService.get_feedback_by_telegram_id(user_id)
        if feedback:
            await message.answer(messages["feedbackExists"], reply_markup=keyboards.getMenuKeyboards(userSettings.LanguageId))
            return

        button_text = "Telefon raqam yuborish☎️" if userSettings.LanguageId == 1 else "Отправить номер телефона☎️"
        button = KeyboardButton(text=button_text, request_contact=True)
    
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[button]],
            resize_keyboard=True, 
            one_time_keyboard=True  
        )

        await state.set_state(CreateFeedback.PhoneNumber)
        await message.answer(messages['askPhone'], reply_markup=keyboard)

    except Exception as e:
        print(f"Error in ask_phone: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())

@router.message(CreateFeedback.PhoneNumber)
async def start_grade(message: types.Message, state: FSMContext):
    try:
        if(message.contact is None):
            await message.answer(messages['invalidInput'])
            return
        
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        await state.update_data(PhoneNumber=message.contact.phone_number)
        await state.set_state(CreateFeedback.WasRude)
        
        await message.answer(messages['wasRude'], reply_markup=keyboards.getYesNoKeyboard(userSettings.LanguageId))
    except Exception as e:
        print(f"Error in start_grade: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())

@router.message(CreateFeedback.WasRude)
async def ask_SentToPrivateClinic(message: types.Message, state: FSMContext):
    try:
        possibleInputs = ['ha', "yo'q", "да", "нет"]
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        if message.text.lower() not in possibleInputs:
            await message.answer(messages['invalidInput'])
            return
        
        wasRudeInput = message.text.lower()
        await state.update_data(WasRude=(wasRudeInput == "ha" or wasRudeInput == "да"))
        await state.set_state(CreateFeedback.SentToPrivateClinic)
        await message.answer(messages['askSentToPrivateClinic'], reply_markup=keyboards.getYesNoKeyboard(userSettings.LanguageId))
    except Exception as e:
        print(f"Error in ask_SentToPrivateClinic: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())

@router.message(CreateFeedback.SentToPrivateClinic)
async def ask_ServiceQuality(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        userInput = message.text.lower()
        await state.update_data(SentToPrivateClinic=(userInput == "ha" or userInput == "да"))
        await state.set_state(CreateFeedback.ServiceQuality)
        await message.answer(messages['serviceQuality'], reply_markup=keyboards.getQualityKeyboards(userSettings.LanguageId))
    except Exception as e:
        print(f"Error in ask_ServiceQuality: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())

@router.message(CreateFeedback.ServiceQuality)
async def ask_DoctorName(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        userInput = message.text.lower()
        possibleInputs = ["yaxshi", "yomon", "juda yomon", "хорошо", "плохо", "очень плохо"]
        if userInput not in possibleInputs:
            await message.answer(messages['invalidInput'])
            return

        if userInput == "yaxshi" or userInput == "хорошо":
            await state.update_data(ServiceQuality=3)
        elif userInput == "yomon" or userInput == "плохо":
            await state.update_data(ServiceQuality=2)
        else:
            await state.update_data(ServiceQuality=1)
            
        await state.set_state(CreateFeedback.DoctorName)
        await message.answer(messages['doctorName'], reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        print(f"Error in ask_DoctorName: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())

@router.message(CreateFeedback.DoctorName)
async def finish_Feedback(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        userSettings = await UserSettingsService.get_by_telegram_id(user_id)
        messages = load_language("uz" if userSettings.LanguageId == 1 else "ru")
        await state.update_data(DoctorName=message.text)
        data = await state.get_data()
        await state.clear()

        data.update({
            'FirstName': message.from_user.first_name,
            'LastName': message.from_user.last_name,
            'TelegramId': user_id
        })
        await FeedbackService.create_feedback(data)
        await message.answer(messages['thanks'], reply_markup=keyboards.getMenuKeyboards(userSettings.LanguageId))
    except Exception as e:
        print(f"Error in finish_Feedback: {e}")
        await message.answer(messages["error"], reply_markup=types.ReplyKeyboardRemove())
