from pyrogram import Client, filters
from Oneforall.utils.decorators.sudo import SudoUsersOnly
from Oneforall.utils.database import superbans
from config import LOG_CHANNEL

@Client.on_message(filters.command("unsuperban"))
@SudoUsersOnly
async def unsuperban(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user.")

    user = message.reply_to_message.from_user
    data = await superbans.find_one({"user_id": user.id})

    if not data:
        return await message.reply_text("User is not superbanned.")

    await superbans.delete_one({"user_id": user.id})

    await message.reply_text(f"♻️ Unsuperbanned {user.mention}")

    await _.send_message(
        LOG_CHANNEL,
        f"♻️ UNSUPERBAN\nUser: `{user.id}`\nBy: {message.from_user.mention}"
    )
