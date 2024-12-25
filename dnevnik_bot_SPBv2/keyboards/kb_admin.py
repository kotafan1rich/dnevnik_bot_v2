from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .kb_client import cancel_b

add_user_b = KeyboardButton(text="Добавить")
update_user_b = KeyboardButton(text="Обновить")
get_user_b = KeyboardButton(text="Получить")


kb_admin_bottoms = [[add_user_b, update_user_b, get_user_b], [cancel_b]]

kb_admin = ReplyKeyboardMarkup(keyboard=kb_admin_bottoms, resize_keyboard=True)

