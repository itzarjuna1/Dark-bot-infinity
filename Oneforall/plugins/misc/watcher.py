from pyrogram import filters, Client
from pyrogram.types import Message

from Oneforall import app
from Oneforall.core.call import Hotty
from Oneforall.core.mongo import is_superbanned_user

# --- Existing watcher groups ---
WELCOME_GROUP = 20
CLOSE_GROUP = 30

@app.on_message(filters.video_chat_started, group=WELCOME_GROUP)
@app.on_message(filters.video_chat_ended, group=CLOSE_GROUP)
async def vc_watcher(_, message: Message):
    await Hotty.stop_stream_force(message.chat.id)


# --- NEW: Superban Enforcer ---
@app.on_message(filters.new_chat_members)
async def superban_enforcer(_, message: Message):
    for user in message.new_chat_members:
        if await is_superbanned_user(user.id):
            # Force ban user if globally superbanned
            await _.ban_chat_member(message.chat.id, user.id)
