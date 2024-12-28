from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from create_bot import bot
from .fsms import FSMSettings
from handlers.session import get_global_session
from handlers.keyboards import (
	change_info_b,
	change_jwt_b,
	education_id_b,
	get_kb_client_main,
	group_id_b,
	kb_client_set_params,
	kb_client_settings,
	save_b,
	settings_b,
	kb_client_cancel,
)
from messages import (
	ADDED,
	CHANGE_SETTINGS,
	ERROR_MES,
	SETTED_SAVE,
	SETTINGS,
)
from handlers.services import (
	MarksService,
)
from .filters import MarksFilter

PERIOD_TEXTS = [
	"1 четверть",
	"2 четверть",
	"3 четверть",
	"4 четверть",
	"I полугодие",
	"II полугодие",
	"Год",
]


marks_router = Router()


@marks_router.message(MarksFilter(), F.text == settings_b.text)
async def get_settings(message: types.Message, state: FSMContext):
	session = await get_global_session()
	id_tg = message.from_user.id
	marks_servise = MarksService(session=session)
	user_info = await marks_servise.get_user_info(id_tg)
	if not user_info:
		marks_servise.add_user(id_tg)
		user_info = await marks_servise.get_user_info(id_tg)
	clean_user_info: str = marks_servise.get_clean_user_info(user_info)

	await state.set_state(FSMSettings.user_info)
	await bot.send_message(
		id_tg,
		f"{SETTINGS}\n{clean_user_info}",
		reply_markup=kb_client_settings,
	)


@marks_router.message(MarksFilter(FSMSettings.user_info), F.text == change_info_b.text)
async def change_info(message: types.Message, state: FSMContext):
	await state.set_state(FSMSettings.change_info)
	await bot.send_message(
		message.from_user.id, CHANGE_SETTINGS, reply_markup=kb_client_set_params
	)


@marks_router.message(
	MarksFilter(FSMSettings.change_info),
	F.text.in_((education_id_b.text, group_id_b.text, change_jwt_b.text, save_b.text)),
)
async def set_settings(message: types.Message, state: FSMContext):
	param = message.text
	id_tg = message.from_user.id

	if param == save_b.text:
		params = await state.get_data()
		session = await get_global_session()
		marks_servise = MarksService(session=session)
		res = await marks_servise.save_user_info(
			id_tg=message.from_user.id, user_info=params
		)
		text = ADDED if res else ERROR_MES
		session = await get_global_session()
		await bot.send_message(
			message.from_user.id,
			text,
			reply_markup=await get_kb_client_main(id_tg, session),
		)
		await state.clear()

	else:
		if param == education_id_b.text:
			await state.set_state(FSMSettings.education_id)
		elif param == group_id_b.text:
			await state.set_state(FSMSettings.group_id)
		elif param == change_jwt_b.text:
			await state.set_state(FSMSettings.jwt_token)
		else:
			return await state.clear()
		await bot.send_message(
			message.from_user.id, f"Введите {param}", reply_markup=kb_client_cancel
		)


@marks_router.message(MarksFilter(FSMSettings.education_id))
async def set_education_id(message: types.Message, state: FSMContext):
	await state.update_data(education_id=int(message.text))
	await state.set_state(FSMSettings.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)


@marks_router.message(MarksFilter(FSMSettings.group_id))
async def set_group_id(message: types.Message, state: FSMContext):
	await state.update_data(group_id=int(message.text))
	await state.set_state(FSMSettings.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)


@marks_router.message(MarksFilter(FSMSettings.jwt_token))
async def set_jwt(message: types.Message, state: FSMContext):
	await state.update_data(jwt_token=message.text)
	await state.set_state(FSMSettings.change_info)
	await bot.send_message(
		message.from_user.id,
		SETTED_SAVE,
		reply_markup=kb_client_set_params,
	)


@marks_router.message(MarksFilter(), F.text.in_(PERIOD_TEXTS))
async def get_marks_handler(message: types.Message):
	id_tg = message.from_user.id
	period = message.text
	session = await get_global_session()
	marks_servise = MarksService(session=session)
	marks = await marks_servise.get_marks(id_tg=id_tg, period=period)
	await bot.send_message(
		message.from_user.id,
		marks,
		reply_markup=await get_kb_client_main(id_tg, session),
	)
