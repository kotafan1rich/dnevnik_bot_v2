from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext



class MarksFilter(Filter):
	def __init__(self, state=None):
		self.state = state

	async def __call__(self, message: Message, state: FSMContext) -> bool:
		text = message.text
		state = await state.get_state()
		return self.state == state


class GetMarksFilter(Filter):
	async def __call__(self, message: Message) -> bool:
		text = message.text
		return "четверть" in text or "полугодие" in text or "Год" in text
