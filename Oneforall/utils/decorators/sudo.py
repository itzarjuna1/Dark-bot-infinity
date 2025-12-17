from functools import wraps
from pyrogram.types import Message
from Oneforall.misc import SUDOERS

def SudoUsersOnly(func):
    """
    Decorator to allow only sudo users to run certain commands.
    Usage:
    @SudoUsersOnly
    async def some_command(client, message):
        ...
    """
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else None
        if user_id not in SUDOERS:
            await message.reply_text("❌ You are not a sudo user!")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper
