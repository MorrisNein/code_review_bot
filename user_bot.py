from typing import Dict, List, Any

import pyrogram
from pyrogram import idle
from pyrogram.types import Message

import config

from config import pyro_client


async def userbot_loop():
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


# async def get_message_mentioned_users(chat_id, message_id):
#     message: Message = await pyro_client.get_messages(chat_id=chat_id, message_ids=message_id)
#     user_ids = [entity.user.id for entity in message.entities]
#     return user_ids