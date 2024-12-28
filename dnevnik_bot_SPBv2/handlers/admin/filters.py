from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .fsms import FSMAdmin


class AdminFilter(Filter):
	admins = (1324716819,)

	def __init__(self, state=None):
		self.state = state or FSMAdmin.admin

	async def __call__(self, message: Message, state: FSMContext) -> bool:
		state = await state.get_state()
		return message.from_user.id in self.admins and self.state == state