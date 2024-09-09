#!/usr/bin/python
# vim: set fileencoding=UTF-8
import asyncio
import logging

from create_bot import bot, dp
from handlers import client

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)


async def main():
	await bot.delete_webhook()
	await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())
