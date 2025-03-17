from DanteUserbot import *
import requests
from pyrogram import Client, filters
from pyrogram.errors import ChatIdInvalid
from pyrogram.errors import (
    ChatAdminRequired,
    ChatNotModified,
    ChatIdInvalid,
    FloodWait,
    InviteHashExpired,
    UserNotParticipant,
)
import os
import json
from pyrogram.types import Message

__MODULE__ = "ʟɪɴᴋ"
__HELP__ = """<blockquote><b>
『 Ambil Link 』

  • perintah: {0}copylink
  • penjelasan: untuk mengambil link digroup Maupun channels.
  • perintah: {0}idlink
  • penjelasan: untuk mengambil link digroup menggunakan id channels dan group.
  EXAMPLE: .givelinkid -100xxxxxxxx</b></blockquote>
"""


@DANTE.UBOT("copylink")
async def copy_link_command(client, message):
    chat = message.chat.id
    try:
        link = await client.export_chat_invite_link(chat)
        await message.reply_text(f"Here's the invite link for this chat:\n{link}")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


@DANTE.UBOT("idlink")
async def idlink_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Penggunaan tidak valid. Format yang benar .givelinkid group_id")
        return

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))

        if chat is None:
            await message.reply("Unable to get information for the specified group ID.")
            return

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except FloodWait as e:
            await message.reply(f"FloodWait: {e.x} seconds. Retrying in {e.x} seconds.")
            return

        group_data = {
            "id": chat.id,
            "type": str(chat.type),
            "title": chat.title,
            "members_count": chat.members_count,
            "description": chat.description,
            "invite_link": invite_link,
            "is_verified": chat.is_verified,
            "is_restricted": chat.is_restricted,
            "is_creator": chat.is_creator,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake,
            "dc_id": chat.dc_id,
            "has_protected_content": chat.has_protected_content,
        }

        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=f"Here is the information for\n{chat.title}\nThe group information scraped by: @{client.username}",
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
