from datetime import datetime

from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
import asyncio
from init_db import create_pool

loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())


class DBCommands:
    """Class for working with DB."""
    pool: Connection = db

    ADD_NEW_USER = "INSERT INTO discord_users (user_id, username, adding_date) VALUES ($1, $2, $3)"
    GET_USERS = "SELECT (username) FROM discord_users"
    GET_USERS_ID = "SELECT (user_id) FROM discord_users"
    COUNT_USERS = "SELECT COUNT (*) FROM discord_users"
    GET_CODE = "SELECT secret_code FROM discord_code"
    GET_CODE_ID = "SELECT id FROM discord_code"
    SET_CODE = "UPDATE discord_code SET secret_code=$1 WHERE id=$2"
    GET_TEXT = "SELECT message FROM discord_texts WHERE action=$1"
    SET_TEXT = "UPDATE discord_texts SET message=$1 WHERE action=$2"

    async def add_new_user(self, data: dict):
        """Add new user to db."""

        command = self.ADD_NEW_USER

        user_id = data.get('user_id')
        username = data.get('username')
        adding_date = datetime.now()

        args = user_id, username, adding_date

        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def count_users(self):
        """Count users in db."""
        command = self.COUNT_USERS
        record = await self.pool.fetchval(command)
        return record

    async def get_code(self):
        """Get secret-code from db."""
        command = self.GET_CODE

        result = await self.pool.fetchval(command)
        if result:
            return result
        else:
            return 'No code available right now'

    async def get_code_id(self):
        """Get id of the secret-code in db."""
        command = self.GET_CODE_ID
        code_id = await self.pool.fetchval(command)
        return code_id

    async def set_code(self, new_code):
        """Update current secret-code in db."""
        command = self.SET_CODE
        return await self.pool.fetchval(command, new_code, await self.get_code_id())

    async def get_users(self):
        """Get all users from the db."""
        command = self.GET_USERS
        data = await self.pool.fetch(command)

        data = [data[i][0] for i in range(len(data))]

        text = ''
        for num, row in enumerate(data):
            text += f'{num + 1}. {row[0]}\n'
        return text

    async def get_users_id(self):
        """Get users in whitelist."""
        command = self.GET_USERS_ID
        data = await self.pool.fetch(command)
        data = [data[i][0] for i in range(len(data))]
        return data

    async def get_text(self, action: str):
        """Get text from db."""
        command = self.GET_TEXT
        text = await self.pool.fetchval(command, action)
        text = text
        return text

    async def set_text(self, text: str, action: str):
        """Update text in db."""
        command = self.SET_TEXT
        args = text, action,
        return await self.pool.fetchval(command, *args)


database = DBCommands()
