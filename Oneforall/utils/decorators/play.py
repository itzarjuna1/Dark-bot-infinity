import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from Oneforall import app, userbot, YouTube
from Oneforall.misc import SUDOERS
from Oneforall.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from Oneforall.utils.inline import botplaylist_markup
from strings import get_string

# Cache invite links
links = {}
clinks = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # Anonymous admin check
        if message.sender_chat:
            return await message.reply_text(
                _["general_3"],
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
                ),
            )

        # Maintenance mode
        if await is_maintenance() and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.\n"
                f"ᴊᴏɪɴ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ</a>",
                disable_web_page_preview=True,
            )

        # Delete command message
        try:
            await message.delete()
        except:
            pass

        # Detect media / URL
        audio_telegram = (
            message.reply_to_message.audio
            or message.reply_to_message.voice
            if message.reply_to_message
            else None
        )
        video_telegram = (
            message.reply_to_message.video
            or message.reply_to_message.document
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)

        # No input
        if not audio_telegram and not video_telegram and not url:
            if len(message.command) < 2:
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        # Channel play mode
        if message.command[0].startswith("c"):
            chat_id = await get_cmode(message.chat.id)
            if not chat_id:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        # Play permissions
        playmode = await get_playmode(message.chat.id)
        playtype = await get_playtype(message.chat.id)

        if playtype != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins or message.from_user.id not in admins:
                return await message.reply_text(_["play_4"])

        # Video mode
        video = (
            True
            if message.command[0].startswith("v") or "-v" in message.text
            else None
        )

        # Force play
        fplay = None
        if message.command[0].endswith("e"):
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True

        # Assistant join logic
        if not await is_active_chat(chat_id):
            current_userbot = await get_assistant(chat_id)
            if not current_userbot:
                return await message.reply_text("❌ Assistant not found.")

            try:
                member = await app.get_chat_member(chat_id, current_userbot.me.id)
                if member.status in (
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ):
                    return await message.reply_text(_["call_2"])
            except UserNotParticipant:
                if chat_id in links:
                    invitelink = links[chat_id]
                else:
                    if message.chat.username:
                        invitelink = message.chat.username
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text(_["call_1"])

                try:
                    await current_userbot.join_chat(invitelink)
                except InviteRequestSent:
                    await app.approve_chat_join_request(chat_id, current_userbot.id)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        _["call_3"].format(app.mention, type(e).__name__)
                    )

                links[chat_id] = invitelink

        # Run original command
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper


def CPlayWrapper(command):
    async def wrapper(client, message):
        i = await client.get_me()
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        if message.sender_chat:
            return await message.reply_text(
                _["general_3"],
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
                ),
            )

        if await is_maintenance() and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                f"{i.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ",
                disable_web_page_preview=True,
            )

        try:
            await message.delete()
        except:
            pass

        audio_telegram = (
            message.reply_to_message.audio
            or message.reply_to_message.voice
            if message.reply_to_message
            else None
        )
        video_telegram = (
            message.reply_to_message.video
            or message.reply_to_message.document
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)

        if not audio_telegram and not video_telegram and not url:
            if len(message.command) < 2:
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["play_18"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        chat_id = message.chat.id
        channel = None

        playmode = await get_playmode(message.chat.id)
        playtype = await get_playtype(message.chat.id)

        if playtype != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins or message.from_user.id not in admins:
                return await message.reply_text(_["play_4"])

        video = True if message.command[0].startswith("v") else None

        fplay = None
        if message.command[0].endswith("e"):
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_16"])
            fplay = True

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
