from aiogram.fsm.state import State, StatesGroup


class FSMSettings(StatesGroup):
	user_info = State()
	change_info = State()
	education_id = State()
	group_id = State()
	jwt_token = State()
