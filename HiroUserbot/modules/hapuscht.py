from pyrogram import Client, filters
import asyncio
import time
from HiroUserbot import *
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram.types import ChatPermissions, Message

@HIRO.UBOT("delallc")
async def deleteall(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.delete(
            message, "__Reply to a message to delete all messages from that user.__"
        )

    HIRO = await client.edit(message, "__Deleting all messages from this user.__")
    user = message.reply_to_message.from_user.id

    await client.delete_user_history(message.chat.id, user)
    await message.delete(HIRO, "__All messages from this user has been deleted.__")

@HIRO.UBOT("unblockall")
async def unblockall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title

    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await client.error(message, f"__Invalid chatId.__\n\n`{e}`")

    HIRO = await client.edit(message, f"__Unblocking all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(chat_id):
        total += 1
        try:
            await client.unblock_user(users.user.id)
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.x)
        except Exception:
            pass

    await client.edit(
        HIRO,
        f"__Unblockall Executed!__ \n\n__Total:__ {total} \n__Unblocked:__ {success} \n__Failed:__ {total - success}",
    )
    await client.check_and_log(
        "unblockall",
        f"**Unblockall In:** {chat_name} \n**Total:** {total} \n**Unblocked:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )
    
