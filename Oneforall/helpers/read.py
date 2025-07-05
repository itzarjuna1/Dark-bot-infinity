from config import OWNER_USERNAME, SUPPORT_GRP
from Oneforall import Oneforall
from pyrogram import Client, filters



name: 🇺🇸 English

# Gban/Unban Section
gban_reason: "ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ɢʙᴀɴ ᴏɴʟʏ ᴡʜᴇɴ ʏᴏᴜ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ʀᴇᴀsᴏɴ ᴛᴏᴏ!!"
ungban_reason: "ᴀs ʏᴏᴜ ɢʙᴀɴɴᴇᴅ!\nᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴜɴɢʙᴀɴ sᴏᴍᴇᴏɴᴇ ᴡɪᴛʜ ʀᴇᴀsᴏɴ ᴏғ ᴜɴɢʙᴀɴɴɪɴɢ!!"
too_short: "ʜᴀʜᴀʜᴀ!!\nɪғ ʏᴏᴜ ᴛʜɪɴᴋ ʙᴏᴛ ᴡɪʟʟ ɢʙᴀɴ ʙʏ ᴀ sɪʟʟʏ ʀᴇᴀsᴏɴ, ᴛʜɪɴᴋ ᴀɢᴀɪɴ. ᴏᴡɴᴇʀ ɪsɴ'ᴛ sᴛᴜᴘɪᴅ!!"

# General Responses
general_1: "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ."
general_2: "ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇꜱ ᴀʀᴇ ᴅᴇᴀᴅ!\n\nᴘʟᴇᴀꜱᴇ ʀᴇᴘᴏʀᴛ @Buyer_infinity ꜰᴏʀ ᴜᴘᴅᴀᴛᴇ."
general_3: "ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.\n\nᴘʟᴇᴀsᴇ sᴡɪᴛᴄʜ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ."
general_4: "» ɴᴏ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ.\n\nReload via /reload"
general_5: "» ʙᴏᴛ ɪs ɴᴏᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ."

# Telegram Download Messages
tg:
  download_status: "<u><b>{0} ᴅᴏᴡɴʟᴏᴀᴅᴇʀ</b></u>\n\n<b>ғɪʟᴇ sɪᴢᴇ :</b> {1}\n<b>ᴄᴏᴍᴘʟᴇᴛᴇᴅ :</b> {2}\n<b>ᴘᴇʀᴄᴇɴᴛᴀɢᴇ :</b> {3}%\n<b>sᴘᴇᴇᴅ :</b> {4}/s\n<b>ᴇᴛᴀ :</b> {5}"
  processing: "sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ, ᴘʀᴏᴄᴇssɪɴɢ ғɪʟᴇ...\n\n<b>ᴛɪᴍᴇ ᴇʟᴀᴘsᴇᴅ :</b> {0}"
  failed: "ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."
  already_done: "» ᴅᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴘʟᴇᴛᴇᴅ."
  cancel_success: "» ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ."
  cancel_by: "» ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ : {0}"
  stop_failed: "ғᴀɪʟᴇᴅ ᴛᴏ sᴛᴏᴘ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ."
  ongoing_failed: "ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴏɴɢᴏɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ."

# Call/Video Chat Errors & Status
call:
  assistant_ban: "<u>{0} ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.</u>\n<b>ɪᴅ :</b> <code>{1}</code>\n<b>ɴᴀᴍᴇ :</b> {2}\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{3}"
  invite_error: "» ʙᴏᴛ ɴᴇᴇᴅs 'ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ' ᴘᴇʀᴍɪssɪᴏɴ."
  inviting: "ᴡᴀɪᴛɪɴɢ...\nɪɴᴠɪᴛɪɴɢ {0} ᴀssɪsᴛᴀɴᴛ."
  joined: "{0} ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ.\nsᴛᴀʀᴛɪɴɢ sᴛʀᴇᴀᴍ..."
  stream_failed: "ғᴀɪʟᴇᴅ ᴛᴏ sᴛʀᴇᴀᴍ. ᴜsᴇ /skip ᴛᴏ ᴛʀʏ ᴀɢᴀɪɴ."
  stream_switch_failed: "ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ. ᴘʟᴇᴀsᴇ /skip."
  no_videochat: "<b>Nᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄ
