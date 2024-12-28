from aiogram import F, Router, types

from .fsms import FSMAdmin, FSMAdminAddUser, FSMAdminGetUser, FSMAdminUpdateUser

from .filters import AdminFilter
from handlers.services import MarksService
from handlers.session import get_global_session
from messages import (
	ADDED,
	ADMIN_PANEL,
	CHANGE_SETTINGS,
	ERROR_MES,
	GET_ID_TG,
	SETTED_SAVE,
	SETTINGS,
	USER_EXISTS,
	USER_DOES_NOT_EXIST,
)
from handlers.keyboards import (
	get_user_b,
	update_user_b,
	add_user_b,
	kb_admin,
	kb_client_set_params,
	save_b,
	education_id_b,
	group_id_b,
	change_jwt_b,
	kb_client_cancel
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from create_bot import bot

admin_router = Router(name="admin_handler")

admins = (1324716819,)


@admin_router.message(Command("admin"), F.from_user.id.in_(admins))
async def admin_panel(message: types.Message, state: FSMContext):
	await state.set_state(FSMAdmin.admin)
	await bot.send_message(message.from_user.id, ADMIN_PANEL, reply_markup=kb_admin)


@admin_router.message(AdminFilter(), F.text == add_user_b.text)
async def add_user(message: types.Message, state: FSMContext):
	await state.set_state(FSMAdminAddUser.id_tg)
	await bot.send_message(message.from_user.id, GET_ID_TG, reply_markup=kb_client_cancel)


@admin_router.message(AdminFilter(FSMAdminAddUser.id_tg))
async def add_user_by_id_tg(message: types.Message, state: FSMContext):
	id_tg = int(message.text)
	session = await get_global_session()
	marks_servise = MarksService(session=session)
	if (
		not await marks_servise.user_exists(id_tg)
		and await marks_servise.add_user(id_tg) == 200
	):
		await bot.send_message(message.from_user.id, ADDED, reply_markup=kb_admin)
	else:
		await bot.send_message(message.from_user.id, USER_EXISTS, reply_markup=kb_admin)
	await state.set_state(FSMAdmin.admin)


@admin_router.message(AdminFilter(), F.text == get_user_b.text)
async def get_user(message: types.Message, state: FSMContext):
	await state.set_state(FSMAdminGetUser.id_tg)
	await bot.send_message(message.from_user.id, GET_ID_TG, reply_markup=kb_client_cancel)


@admin_router.message(AdminFilter(FSMAdminGetUser.id_tg))
async def get_user_by_id_tg(message: types.Message, state: FSMContext):
	id_tg = int(message.text)
	session = await get_global_session()
	marks_servise = MarksService(session=session)
	user_info = await marks_servise.get_user_info(id_tg)
	if not user_info:
		await bot.send_message(message.from_user.id, USER_DOES_NOT_EXIST, reply_markup=kb_admin)
	else:
		clean_user_info: str = marks_servise.get_clean_user_info(user_info)
		await bot.send_message(
			message.from_user.id,
			f"{SETTINGS}\n{clean_user_info}",
			reply_markup=kb_admin,
		)

	await state.set_state(FSMAdmin.admin)


@admin_router.message(AdminFilter(), F.text == update_user_b.text)
async def change_info_admin(message: types.Message, state: FSMContext):
	await state.set_state(FSMAdminUpdateUser.id_tg)
	await bot.send_message(message.from_user.id, GET_ID_TG, reply_markup=kb_client_cancel)


@admin_router.message(AdminFilter(FSMAdminUpdateUser.id_tg))
async def get_id_tg_admin(message: types.Message, state: FSMContext):
	await state.update_data(id_tg=int(message.text))
	await state.set_state(FSMAdminUpdateUser.change_info)
	await bot.send_message(
		message.from_user.id, CHANGE_SETTINGS, reply_markup=kb_client_set_params
	)


@admin_router.message(
	AdminFilter(FSMAdminUpdateUser.change_info),
	F.text.in_((education_id_b.text, group_id_b.text, change_jwt_b.text, save_b.text)),
)
async def set_settings_admin(message: types.Message, state: FSMContext):
	param = message.text
	if param == save_b.text:
		session = await get_global_session()
		fsm_data = await state.get_data()
		id_tg = fsm_data["id_tg"]
		fsm_data.pop("id_tg")
		marks_servise = MarksService(session=session)
		res = await marks_servise.save_user_info(id_tg=id_tg, user_info=fsm_data)
		text = ADDED if res else ERROR_MES
		session = await get_global_session()
		await bot.send_message(message.from_user.id, text, reply_markup=kb_admin)
		await state.set_state(FSMAdmin.admin)

	else:
		if param == education_id_b.text:
			await state.set_state(FSMAdminUpdateUser.education_id)
		elif param == group_id_b.text:
			await state.set_state(FSMAdminUpdateUser.group_id)
		elif param == change_jwt_b.text:
			await state.set_state(FSMAdminUpdateUser.jwt_token)
		else:
			return await state.clear()
		await bot.send_message(
			message.from_user.id, f"Введите {param}", reply_markup=kb_client_cancel
		)


@admin_router.message(AdminFilter(FSMAdminUpdateUser.education_id))
async def set_education_id_admin(message: types.Message, state: FSMContext):
	await state.update_data(education_id=int(message.text))
	await state.set_state(FSMAdminUpdateUser.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)


@admin_router.message(AdminFilter(FSMAdminUpdateUser.group_id))
async def set_group_id_admin(message: types.Message, state: FSMContext):
	await state.update_data(group_id=int(message.text))
	await state.set_state(FSMAdminUpdateUser.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)


@admin_router.message(AdminFilter(FSMAdminUpdateUser.jwt_token))
async def set_jwt_admin(message: types.Message, state: FSMContext):
	await state.update_data(jwt_token=message.text)
	await state.set_state(FSMAdminUpdateUser.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)
