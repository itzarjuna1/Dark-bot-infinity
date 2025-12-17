from pyrogram import filters
from Oneforall import app

from Oneforall.utils.decorators.admins import AdminRightsCheck
from Oneforall.utils.database import (
    add_superban_user,
    remove_superban_user,
    is_superbanned_user,
)
from config import LOG_CHANNEL, SUPERBAN_VIDEO

from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name="DarkInfinity")


@Client.on_message(filters.command("superban") & filters.group)
@AdminRightsCheck
async def superban(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to superban.")

    user = message.reply_to_message.from_user

    if await is_superbanned_user(user.id):
        return await message.reply_text("🚫 User is already superbanned.")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Confirm", callback_data=f"sb_yes_{user.id}"
                ),
                InlineKeyboardButton(
                    "❌ Cancel", callback_data="sb_no"
                ),
            ]
        ]
    )

    await message.reply_text(
        f"⚠️ **Confirm SUPERBAN**\n\n👤 {user.mention}",
        reply_markup=buttons,
    )


@Client.on_callback_query(filters.regex("^sb_yes_"))
async def superban_confirm(_, cq):
    user_id = int(cq.data.split("_")[-1])
    chat = cq.message.chat

    await _.ban_chat_member(chat.id, user_id)

    await add_superban_user(
        user_id=user_id,
        banned_by=cq.from_user.id,
    )

    page = telegraph.create_page(
        title="Superban Executed",
        html_content=f"""
        <video controls>
        <source src="{SUPERBAN_VIDEO}" type="video/mp4">
        </video>
        """,
    )

    await _.send_message(
        LOG_CHANNEL,
        f"""
🚫 **SUPERBAN EXECUTED**
👤 User ID: `{user_id}`
👮 By: {cq.from_user.mention}
📍 Chat: {chat.title}
📹 {page['url']}
""",
    )

    await cq.message.edit_text("🚫 **Superban executed successfully. superbanned user have been nicely pissed of by the administers**")


@Client.on_callback_query(filters.regex("^sb_no$"))
async def superban_cancel(_, cq):
    await cq.message.edit_text("❌ Superban cancelled.")
