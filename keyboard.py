import random
from typing import Optional, Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from wordings import w_choose_developer_buttons, w_close_keyboard, w_temporary_keyboard


class ChooseDeveloperRankKeyboardDispatcher:
    def __init__(self, inline_keyboard_markup: Optional[InlineKeyboardMarkup] = None):
        self.keyboard = inline_keyboard_markup or self.create_keyboard()

    @classmethod
    def create_keyboard(cls):
        keyboard = InlineKeyboardMarkup()
        emoji_0, emoji_1 = random.choice(w_choose_developer_buttons)
        keyboard.row(
            InlineKeyboardButton(text=emoji_0, callback_data=cls.get_button_callback_data(dev_rank=0, click_count=0)),
            InlineKeyboardButton(text=emoji_1, callback_data=cls.get_button_callback_data(dev_rank=1, click_count=0))
        )
        keyboard.row(InlineKeyboardButton(text=random.choice(w_close_keyboard), callback_data='close_dev_choice'))
        return keyboard

    def update_button_click(self, dev_rank):
        button: InlineKeyboardButton = self.keyboard.inline_keyboard[0][dev_rank]
        dev_rank, click_count = self.dispatch_callback_data(button.callback_data)
        button.callback_data = self.get_button_callback_data(dev_rank=dev_rank, click_count=click_count + 1)
        if click_count == 0:
            button.text = ' '.join([str(click_count + 1), button.text])
        else:
            button.text = button.text.replace(str(click_count), str(click_count + 1))

    @staticmethod
    def dispatch_callback_data(callback_data: str) -> Tuple[int, int]:
        _, dev_rank, click_count = callback_data.split(':')
        return int(dev_rank), int(click_count)

    @staticmethod
    def get_button_callback_data(dev_rank: int, click_count: int = 0):
        return f'choose_dev:{dev_rank}:{click_count}'


def tmp_keyboard(function):
    """Replaces message's keyboard with a temporary one until processing is finished"""
    async def wrapper(*args, **kwargs):
        message = args[0]
        if isinstance(message, CallbackQuery):
            message = message.message

        old_keyboard_buffer = message.reply_markup
        temporary_keyboard = InlineKeyboardMarkup()
        temporary_keyboard.row(InlineKeyboardButton(text=random.choice(w_temporary_keyboard), callback_data='tmp'))
        await message.edit_reply_markup(temporary_keyboard)

        try:
            result = await function(*args, **kwargs)
        finally:
            if message.reply_markup == temporary_keyboard:
                await message.edit_reply_markup(old_keyboard_buffer)

        return result
    return wrapper
