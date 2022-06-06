import os

import pyrogram
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

# from aiogram.contrib.fsm_storage.redis import RedisStorage2
# from throttling_middleware import ThrottlingMiddleware  # - Redis required

_config = {
    **dotenv_values('.env'),  # load values from file
    # **os.environ  # override loaded values with environment variables
}

TECH_SUPPORT_ID = [int(id_) for id_ in _config['TECH_SUPPORT_ID'].split(' ')]
CHAT_ID = int(_config.get('CHAT_ID'))
BOT_USERNAME = _config.get('BOT_USERNAME')

bot = Bot(token=_config['BOT_TOKEN'])
# storage = RedisStorage2()
dp = Dispatcher(
    bot,
    # storage=storage
)
# dp.middleware.setup(ThrottlingMiddleware())
pyro_client = pyrogram.Client(BOT_USERNAME, _config['TELEGRAM_API_ID'], _config['TELEGRAM_API_HASH'])
