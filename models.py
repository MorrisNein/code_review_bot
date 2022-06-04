from typing import Optional, List

from pyrogram.types import User as TelegramUser, ChatMember

from data_manager import db


class DeveloperRanks:
    JUNIOR = 0
    SENIOR = 1


class User:
    def __init__(self, user_id: int, safe=False):
        if not user_id:
            raise ValueError

        user = self.find(user_id=user_id)
        if not user:
            if safe:
                self.data = {}
                return
            raise ValueError

        self.data = user

    @classmethod
    def new(cls, user_id: int, username: str, is_developer: bool = True,
            developer_rank: int = DeveloperRanks.JUNIOR, reviews_count: int = 0):
        user = db.users.find_one(user_id=user_id)
        if user is None:
            db.users.update_one(user_id, {
                'is_developer': is_developer,
                'username': username,
                'developer_rank': developer_rank,
                'reviews_count': reviews_count
            })

    def update(self):
        db.users.update_one(self.data['user_id'], self.data)

    @classmethod
    def find(cls, user_id: int):
        return db.users.find_one(user_id)

    @classmethod
    def create_from_telegram_user(cls, telegram_user: TelegramUser):
        user = cls(user_id=telegram_user.id, safe=True)
        user_data = {
            'user_id': telegram_user.id,
            'username': telegram_user.username,
            'is_developer': not telegram_user.is_bot
        }
        if not user.data:
            cls.new(**user_data)
        else:
            user.data.update(user_data)
            user.update()

    @classmethod
    def get_developers(cls, rank: int = DeveloperRanks.JUNIOR, exclude_user_ids: Optional[List[int]] = None,
                       exclude_usernames: Optional[List[str]] = None):
        exclude_user_ids = exclude_user_ids or []
        developers = []
        for user_data in db.users.data.values():
            if user_data.get('is_developer') and user_data.get('developer_rank') == rank \
                    and user_data.get('user_id') not in exclude_user_ids \
                    and user_data.get('username') not in exclude_usernames:
                developers.append(user_data)
        return developers


def is_user_developer(user: TelegramUser):
    return not user.is_bot


def get_full_name(first_name: Optional[str], last_name: Optional[str], username: Optional[str] = None):
    if first_name and last_name:
        name = ' '.join([first_name, last_name])
    elif first_name:
        name = first_name
    elif last_name:
        name = last_name
    else:
        name = username

    return name


def update_users_list(members_list: List[ChatMember]):
    for member in members_list:
        User.create_from_telegram_user(member.user)
