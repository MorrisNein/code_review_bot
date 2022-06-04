import os

import pyrogram
from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from throttling_middleware import ThrottlingMiddleware

TECH_SUPPORT_ID = [406584268]
CHAT_ID = int(os.environ['CHAT_ID'])
BOT_USERNAME = os.environ['BOT_USERNAME']

# Bot
bot = Bot(token=os.environ['BOT_TOKEN'])
# storage = RedisStorage2()
dp = Dispatcher(bot)
# dp.middleware.setup(ThrottlingMiddleware())


# User Bot
pyro_client = pyrogram.Client(BOT_USERNAME, os.environ['TELEGRAM_API_ID'], os.environ['TELEGRAM_API_HASH'])
