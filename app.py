import asyncio
import logging
import random

from aiogram import executor
from aiogram.types import ContentTypes, Message, CallbackQuery

from async_lock import async_lock
from config import bot, dp
from keyboard import ChooseDeveloperRankKeyboardDispatcher, tmp_keyboard
from models import User, get_full_name, update_users_list, DeveloperRanks
from user_bot import get_chat_members_list, get_users_attributes, run_userbot
from wordings import *

logging.basicConfig(level=logging.INFO)


async def delete_message_with_delay(message: Message):
    await message.edit_text(
        random.choice(w_delete_message),
        reply_markup=None,
    )
    await asyncio.sleep(5)
    await message.delete()


@dp.callback_query_handler(lambda callback: callback.data.startswith('close_dev_choice'))
async def close_dev_choice(callback: CallbackQuery, **kwargs):
    message = callback.message
    await delete_message_with_delay(message)


@dp.callback_query_handler(lambda callback: callback.data.startswith('choose_dev'))
@tmp_keyboard
@async_lock
async def choose_developer(callback: CallbackQuery, **kwargs):
    callback_message = callback.message
    pr_message = callback_message.reply_to_message

    keyboard_dispatcher = ChooseDeveloperRankKeyboardDispatcher(callback_message.reply_markup)
    dev_rank, _ = keyboard_dispatcher.dispatch_callback_data(callback.data)
    keyboard_dispatcher.update_button_click(dev_rank)

    users_already_picked = [username.strip() for username in callback_message.text.split('@')[1:]]

    update_users_list(await get_chat_members_list())
    developers = User.get_developers(
        dev_rank,
        exclude_user_ids=[pr_message.from_user.id],
        exclude_usernames=users_already_picked
    )

    if len(developers) == 0:
        dev_rank_str = {
            DeveloperRanks.JUNIOR: 'младшего',
            DeveloperRanks.SENIOR: 'старшего',
        }
        await pr_message.reply(f'Не удалось найти {dev_rank_str[dev_rank]} разработчика.')
        await delete_message_with_delay(callback_message)
        return

    sample_size = min(6, len(developers))

    developers = random.sample(developers, sample_size)
    developers = await get_users_attributes(developers, ['username', 'first_name', 'last_name'])

    callback_user = callback.from_user
    text = f'{get_full_name(callback_user.first_name, callback_user.last_name)} запустил жребий.\n\n'

    for number, developer in enumerate(developers, start=1):
        developer_name = get_full_name(developer['first_name'], developer['last_name'], developer['username'])
        text += f'{number}. {developer_name}\n'

    await pr_message.reply(text)

    await asyncio.sleep(2)

    dice_message = await pr_message.answer_dice()
    dice_value = dice_message.dice.value - 1

    await asyncio.sleep(5)
    winner = developers[dice_value % sample_size]['username']

    await pr_message.reply(text=random.choice(w_the_chosen_one).format(winner))
    await callback_message.edit_text(f'{callback_message.text}\n@{winner}', reply_markup=keyboard_dispatcher.keyboard)


@dp.message_handler(lambda m: m.chat.id == config.CHAT_ID, content_types=ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: Message, **kwargs):
    for user in message.new_chat_members:
        User.create_from_telegram_user(user)


@dp.message_handler(lambda m: m.chat.id == config.CHAT_ID, content_types=ContentTypes.LEFT_CHAT_MEMBER)
async def left_chat_member(message: Message, **kwargs):
    user_id = message.left_chat_member.id
    if User.find(user_id) is None:
        return
    user = User(user_id)
    user.data['is_developer'] = False
    user.update()


@dp.message_handler(lambda m: m.chat.id != config.CHAT_ID and m.from_user.id in config.TECH_SUPPORT_ID,
                    commands=['update_users_list'])
async def update_users_list_command(message: Message, **kwargs):
    update_users_list(await get_chat_members_list())
    await message.reply('Success!')


@dp.message_handler(commands=['help', 'start'])
async def help_start_command(message: Message, **kwargs):
    await introduce_bot(message.chat.id)


async def introduce_bot(chat_id):
    await bot.send_message(chat_id=chat_id, text=w_introduction_text)


@dp.message_handler(commands=['help_tech'])
async def help_tech_command(message: Message, **kwargs):
    await bot.send_message(message.chat.id, w_help_tech)


@dp.message_handler(lambda m: m.chat.id == config.CHAT_ID and f'@{config.BOT_USERNAME}' in m.text)
async def choose_developers_rank(message: Message, **kwargs):
    if message.reply_to_message:
        message = message.reply_to_message

    keyboard = ChooseDeveloperRankKeyboardDispatcher().keyboard
    await message.reply(
        text=random.choice(w_choose_developer),
        reply_markup=keyboard
    )


async def run_bot():
    await dp.start_polling()


async def main():
    await asyncio.gather(
        run_bot(),
        run_userbot(),
    )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

