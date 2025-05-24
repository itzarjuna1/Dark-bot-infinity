import asyncio
import random

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import Message

from Oneforall import app
from Oneforall import userbot as us
from Oneforall.core.userbot import assistants


@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    # Send initial processing message
    processing_msg = await message.reply("<code>Processing...</code>")

    # Check if the user is passed as reply or as argument
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await processing_msg.edit("Usage: <code>/sg [username/user_id] or reply to a user</code>")

    # Try to get the user object
    try:
        user = await client.get_users(user_id)
    except Exception:
        return await processing_msg.edit("<code>Invalid user specified.</code>")

    # Choose one of the sangmata bots randomly
    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    selected_bot = random.choice(sangmata_bots)

    # Select the userbot assistant
    if 1 in assistants:
        ubot = us.one
    else:
        return await processing_msg.edit("<code>Userbot assistant not found.</code>")

    # Send the user ID to the bot
    try:
        sent_msg = await ubot.send_message(selected_bot, str(user.id))
        await sent_msg.delete()
    except Exception as e:
        return await processing_msg.edit(f"<code>{str(e)}</code>")

    await asyncio.sleep(1)

    # Search for the bot's reply
    found = False
    async for msg in ubot.search_messages(selected_bot):
        if msg and msg.text:
            await message.reply(msg.text)
            found = True
            break

    if not found:
        await message.reply("The bot did not return any data.")

    # Try to clear the message history with the bot
    try:
        peer = await ubot.resolve_peer(selected_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    # Remove the processing message
    await processing_msg.delete()