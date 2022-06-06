from typing import Dict, List, Any

from pyrogram import idle

import config
from config import pyro_client


async def run_userbot():
    await pyro_client.start()
    await idle()
    await pyro_client.stop()


async def get_chat_members_list(chat_id: int = config.CHAT_ID) -> list:
    chat_members = []
    async for member in pyro_client.get_chat_members(chat_id):
        chat_members.append(member)
    return chat_members


async def get_users_attributes(users_list, attributes) -> List[Dict[str, Any]]:
    users = await pyro_client.get_users([user['user_id'] for user in users_list])
    names_list = [{attribute: user.__getattribute__(attribute) for attribute in attributes} for user in users]
    return names_list
