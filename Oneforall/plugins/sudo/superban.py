from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Oneforall.decorators.admins import AdminsOnly
from Oneforall.utils.database import superbans
from Oneforall.config import LOG_CHANNEL
from Oneforall.utils.telegraph import upload_video

@Client.on_message(filters.command("superban") & filters.group)
@AdminsOnly
async def superban(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user.")

    user = message.reply_to_message.from_user

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirm", callback_data=f"sb_yes_{user.id}"),
            InlineKeyboardButton("❌ Cancel", callback_data="sb_no")
        ]]
    )

    await message.reply_text(
        f"⚠️ Confirm Superban?\n\n👤 {user.mention}",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("sb_yes_"))
async def confirm_superban(_, cq):
    user_id = int(cq.data.split("_")[-1])
    chat = cq.message.chat

    await _.ban_chat_member(chat.id, user_id)

    await superbans.insert_one({"user_id": user_id})

    telegraph_url = upload_video(
        "https://files.catbox.moe/9l6q0x.mp4"  # example video
    )

    await _.send_message(
        LOG_CHANNEL,
        f"🚫 SUPERBANNED\nUser ID: `{user_id}`\nChat: {chat.title}\n📹 {telegraph_url}"
    )

    await cq.message.edit_text("🚫 Superban executed.")


@Client.on_callback_query(filters.regex("sb_no"))
async def cancel_superban(_, cq):
    await cq.message.edit_text("❌ Superban cancelled.")
