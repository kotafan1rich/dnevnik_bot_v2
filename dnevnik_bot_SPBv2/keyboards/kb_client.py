import aiohttp
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import API_URL

help_b = KeyboardButton(text="Помощь")
settings_b = KeyboardButton(text="Настройки")
cancel_b = KeyboardButton(text="Отмена")
change_info_b = KeyboardButton(text="Изменить информацию")
education_id_b = KeyboardButton(text="education_id")
group_id_b = KeyboardButton(text="group_id")
save_b = KeyboardButton(text="Сохранить")
change_jwt_b = KeyboardButton(text="jwt")


async def get_kb_clent_periods_bottoms(id_tg):
	async with aiohttp.ClientSession() as session:
		params = {"id_tg": id_tg}
		async with session.get(
			f"{API_URL}/marks/get_user_periods", params=params
		) as response:
			data: dict = await response.json()
			return [KeyboardButton(text=period) for period in data.get("result").keys()]


async def get_kb_client_main(id_tg):
	periods = await get_kb_clent_periods_bottoms(id_tg)
	kb_bottoms = [periods, [settings_b, help_b]]
	return ReplyKeyboardMarkup(keyboard=kb_bottoms, resize_keyboard=True)

kb_client_settings_bottms = [[change_info_b], [cancel_b]]

kb_client_set_params_bottms = [
	[education_id_b, group_id_b, change_jwt_b],
	[save_b],
	[cancel_b],
]

kb_client_settings = ReplyKeyboardMarkup(
	keyboard=kb_client_settings_bottms, resize_keyboard=True
)
kb_client_set_params = ReplyKeyboardMarkup(
	keyboard=kb_client_set_params_bottms, resize_keyboard=True
)
