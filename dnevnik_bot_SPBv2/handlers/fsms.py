from aiogram.fsm.state import State, StatesGroup


class FSMAdmin(StatesGroup):
	admin = State()


class FSMAdminAddUser(StatesGroup):
	id_tg = State()


class FSMAdminGetUser(StatesGroup):
	id_tg = State()


class FSMAdminUpdateUser(StatesGroup):
	user_info = State()
	change_info = State()
	id_tg = State()
	education_id = State()
	group_id = State()
	jwt_token = State()


class FSMSettings(StatesGroup):
    user_info = State()
    change_info = State()
    education_id = State()
    group_id = State()
    jwt_token = State()
