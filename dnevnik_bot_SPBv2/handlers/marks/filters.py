from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext



class MarksFilter(Filter):
	def __init__(self, state=None):
		self.state = state

	async def __call__(self, message: Message, state: FSMContext) -> bool:
		state = await state.get_state()
		return self.state == state
