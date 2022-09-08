from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

keyboard_empty = ReplyKeyboardMarkup()

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(KeyboardButton("Настройки⚙️"))
keyboard_main.add(KeyboardButton("Обновить🔃"))

keyboard_inline_properties = InlineKeyboardMarkup()
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить рабочую сумму",
    callback_data="change_value"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить минимальный доход",
    callback_data="change_min_spread"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить мин хороших комментов",
    callback_data="change_min_good"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить макс плохих комментов",
    callback_data="change_max_bad"
))
