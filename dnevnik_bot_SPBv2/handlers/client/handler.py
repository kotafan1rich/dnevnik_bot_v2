from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from create_bot import bot
from handlers.session import get_global_session
from handlers.keyboards import (
	cancel_b,
	get_kb_client_main,
	help_b,
)
from messages import (
	CANCELED,
	HELLO_MES,
	HELP,
)

from handlers.services import (
	MarksService,
)


client_router = Router(name="client_handler")


@client_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
	id_tg = message.from_user.id
	session = await get_global_session()
	marks_servise = MarksService(session=session)
	if not await marks_servise.user_exists(id_tg) and await marks_servise.add_user(
		id_tg
	):
		await bot.send_message(
			id_tg,
			HELLO_MES,
			reply_markup=await get_kb_client_main(id_tg, session),
		)
	else:
		await bot.send_message(
			id_tg,
			HELP,
			reply_markup=await get_kb_client_main(id_tg, session),
			parse_mode=None,
		)


@client_router.message(F.text == cancel_b.text)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
	user_id = message.from_user.id
	session = await get_global_session()

	current_state = await state.get_state()
	if current_state is not None:
		await state.clear()
	await message.answer(
		CANCELED,
		reply_markup=await get_kb_client_main(user_id, session),
	)


@client_router.message(F.text == help_b.text)
async def help(message: types.Message):
	id_tg = message.from_user.id
	session = await get_global_session()

	await bot.send_message(
		message.from_user.id,
		HELP,
		reply_markup=await get_kb_client_main(id_tg, session),
		parse_mode=None,
	)
