from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
import logging
from core.settings import settings
from core.handlers.basic import get_start, parse


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='The bot is launched!')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped!')

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(parse)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())