from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Baxolash⭐️")],
        [KeyboardButton(text="Tilni o'zgartirish⚙️")]
    ]
)

main_menu_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Оценка⭐️")],
        [KeyboardButton(text="Изменить язык⚙️")]
    ]
)

def getMenuKeyboards(langId):
    return main_menu_uz if langId == 1 else main_menu_ru

def getYesNoKeyboard(langId=1):
    if langId == 1:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q")],
            ]
        )
    else:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="Да"), KeyboardButton(text="Нет")],
            ]
        )

def getQualityKeyboards(langId=1):
    if langId == 1:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="yaxshi")],
                [KeyboardButton(text="yomon")],
                [KeyboardButton(text="juda yomon")],
            ]
        )
    else:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text="хорошо")],
                [KeyboardButton(text="плохо")],
                [KeyboardButton(text="очень плохо")],
            ]
        )

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Uz🇺🇿",
                callback_data="uz"
            ),
            InlineKeyboardButton(
                text="ру🇷🇺",
                callback_data="ru"
            ),
        ]
    ]
)