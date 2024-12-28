#!/usr/bin/python
# vim: set fileencoding=UTF-8
import asyncio
import logging

from create_bot import bot, dp
from handlers.admin.handler import admin_router
from handlers.client.handler import client_router
from handlers.marks.handler import marks_router

logging.basicConfig(level=logging.INFO)

dp.include_router(client_router)
dp.include_router(admin_router)
dp.include_router(marks_router)


async def main():
	await bot.delete_webhook()
	await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())
