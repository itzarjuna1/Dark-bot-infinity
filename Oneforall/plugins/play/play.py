import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS, lyrical
from Oneforall import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from Oneforall.core.call import Hotty
from Oneforall.utils import seconds_to_min, time_to_seconds
from Oneforall.utils.channelplay import get_channeplayCB
from Oneforall.utils.decorators.language import languageCB
from Oneforall.utils.decorators.play import PlayWrapper
from Oneforall.utils.formatters import formats
from Oneforall.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from Oneforall.utils.logger import play_logs
from Oneforall.utils.stream.stream import stream


# ================= PLAY COMMAND ================= #

@app.on_message(
    filters.command(
        [
            "play", "vplay", "cplay", "cvplay",
            "playforce", "vplayforce", "cplayforce", "cvplayforce"
        ]
    )
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    # ----- SAFETY -----
    if not message.from_user:
        return await message.reply_text(
            "❌ Anonymous admins are not supported.\nDisable anonymous admin mode."
        )

    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"

    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )

    plist_id = None
    plist_type = None
    spotify = None
    slider = None

    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )

    # ================= TELEGRAM AUDIO ================= #
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])

        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
            )

        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if not await Telegram.download(_, message, mystic, file_path):
            return

        details = {
            "title": await Telegram.get_filename(audio_telegram, audio=True),
            "link": await Telegram.get_link(message),
            "path": file_path,
            "dur": await Telegram.get_duration(audio_telegram, file_path),
        }

        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                streamtype="telegram",
                forceplay=fplay,
            )
        except Exception as e:
            return await mystic.edit_text(
                e if type(e).__name__ == "AssistantErr"
                else _["general_2"].format(type(e).__name__)
            )

        await mystic.delete()
        return await play_logs(message, "Telegram")

    # ================= TELEGRAM VIDEO ================= #
    if video_telegram:
        if message.reply_to_message.document:
            try:
                if video_telegram.file_name.split(".")[-1].lower() not in formats:
                    return await mystic.edit_text(
                        _["play_7"].format(" | ".join(formats))
                    )
            except Exception:
                return await mystic.edit_text(
                    _["play_7"].format(" | ".join(formats))
                )

        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])

        file_path = await Telegram.get_filepath(video=video_telegram)
        if not await Telegram.download(_, message, mystic, file_path):
            return

        details = {
            "title": await Telegram.get_filename(video_telegram),
            "link": await Telegram.get_link(message),
            "path": file_path,
            "dur": await Telegram.get_duration(video_telegram, file_path),
        }

        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=True,
                streamtype="telegram",
                forceplay=fplay,
            )
        except Exception as e:
            return await mystic.edit_text(
                e if type(e).__name__ == "AssistantErr"
                else _["general_2"].format(type(e).__name__)
            )

        await mystic.delete()
        return await play_logs(message, "Telegram Video")

    # ================= URL / SEARCH ================= #
    if not url:
        if len(message.command) < 2:
            return await mystic.edit_text(
                _["play_18"],
                reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)),
            )

        slider = True
        query = message.text.split(None, 1)[1].replace("-v", "")

        try:
            details, track_id = await YouTube.track(query)
        except Exception:
            return await mystic.edit_text(_["play_3"])

        streamtype = "youtube"

    else:
        try:
            await Hotty.stream_call(url)
        except NoActiveGroupCall:
            await mystic.edit_text(_["black_9"])
            return await app.send_message(config.LOGGER_ID, _["play_17"])
        except Exception as e:
            return await mystic.edit_text(_["general_2"].format(type(e).__name__))

        await mystic.edit_text(_["str_2"])

        try:
            await stream(
                _,
                mystic,
                user_id,
                url,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype="index",
                forceplay=fplay,
            )
        except Exception as e:
            return await mystic.edit_text(
                e if type(e).__name__ == "AssistantErr"
                else _["general_2"].format(type(e).__name__)
            )

        return await play_logs(message, "M3U8 / Index")

    # ================= FINAL STREAM ================= #
    try:
        await stream(
            _,
            mystic,
            user_id,
            details,
            chat_id,
            user_name,
            message.chat.id,
            video=video,
            streamtype=streamtype,
            spotify=spotify,
            forceplay=fplay,
        )
    except Exception as e:
        return await mystic.edit_text(
            e if type(e).__name__ == "AssistantErr"
            else _["general_2"].format(type(e).__name__)
        )

    await mystic.delete()
    return await play_logs(message, streamtype)


# ================= CALLBACK: INLINE PLAY ================= #

@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@languageCB
async def play_music(client, CallbackQuery, _):
    if not CallbackQuery.from_user:
        return

    data = CallbackQuery.data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = data.split("|")

    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(_["playcb_1"], show_alert=True)

    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception:
        return

    await CallbackQuery.message.delete()
    await CallbackQuery.answer()

    mystic = await CallbackQuery.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )

    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text(_["play_3"])

    if details["duration_min"]:
        if time_to_seconds(details["duration_min"]) > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
            )

    video = mode == "v"
    ffplay = fplay == "f"

    try:
        await stream(
            _,
            mystic,
            CallbackQuery.from_user.id,
            details,
            chat_id,
            CallbackQuery.from_user.first_name,
            CallbackQuery.message.chat.id,
            video=video,
            streamtype="youtube",
            forceplay=ffplay,
        )
    except Exception as e:
        return await mystic.edit_text(
            e if type(e).__name__ == "AssistantErr"
            else _["general_2"].format(type(e).__name__)
        )

    await mystic.delete()


# ================= CALLBACK: ANONYMOUS ADMIN ================= #

@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)
async def anonymous_admin_alert(client, CallbackQuery):
    await CallbackQuery.answer(
        "Disable anonymous admin mode to use music commands.",
        show_alert=True,
            )
