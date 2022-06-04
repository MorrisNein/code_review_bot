import hashlib
import json
import os
from pathlib import Path
from typing import Optional


class JSONStorage:
    json_file_path: Optional[Path] = None
    data: Optional[dict] = None

    def __init__(self):
        if self.json_file_path is None:
            raise NotImplementedError

        if not os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'w') as file:
                json.dump({}, file)

        self.update_json()

    # Updating information
    def update_json(self):
        self.data = self.read_json()

    # Returns dict with data from json file
    def read_json(self) -> dict:
        with open(self.json_file_path) as readFile:
            dataFromJson = json.load(readFile)
        return dataFromJson

    # Writing information to a file
    def write_json(self):
        with open(self.json_file_path, 'w') as writeFile:
            json.dump(self.data, writeFile, indent=4, ensure_ascii=False)


class UsersDataManager(JSONStorage):
    json_file_path = Path('data', 'users_data.json')

    def find_one(self, user_id: int):
        self.update_json()
        user = self.data.get(str(user_id))
        return user

    def update_one(self, user_id: int, user: dict):
        self.update_json()
        user['user_id'] = user_id
        self.data[str(user_id)] = user
        self.write_json()

    def delete_one(self, user_id: int):
        self.update_json()
        if user_id in self.data:
            del self.data[str(user_id)]
        self.write_json()


class CallbackDataManager(JSONStorage):
    """Handles Telegram's 64-bit limit for callback query"""

    json_file_path = "callback_hash.json"

    def get_hash_by_data(self, callback_data):
        hash_ = hashlib.md5(callback_data.encode('utf-8')).hexdigest()
        self.data[hash_] = callback_data
        self.write_json()
        return hash_

    def get_data_by_hash(self, hash_):
        callback_data = self.data[hash_]
        return callback_data

    def clear_hash(self, hash_):
        if hash_ not in self.data:
            return
        del self.data[hash_]
        self.write_json()


class Database:
    users = UsersDataManager()


db = Database()
