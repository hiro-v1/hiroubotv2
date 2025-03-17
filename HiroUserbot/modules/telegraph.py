from HiroUserbot import *
import requests
from pyrogram import Client, filters

__MODULE__ = "ᴛɢʀᴀᴘʜ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴛᴇʟᴇɢʀᴀᴘʜ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}tg</code> [ʀᴇᴘʟʏ ᴍᴇᴅɪᴀ/ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴘʟᴏᴀᴅ ᴍᴇᴅɪᴀ/ᴛᴇxᴛ ᴋᴇ ᴛᴇʟᴇɢʀᴀ.ᴘʜ
</b></blockquote>"""

API_KEY = "539d3ecbc26d8be7519bb2c64b08da76"

def upload_media_to_imgbb(media_path):
  url = "https://api.imgbb.com/1/upload"
  key = API_KEY
  with open(media_path, 'rb') as file:
    response = requests.post(url, data={'key': key}, files={'image': file})
    if response.status_code == 200:
      return response.json().get("data", {}).get("url", None)
    else:
      return None


@HIRO.UBOT("tg")
async def link_media_handler(client, message):
    media_path = None
    if message.reply_to_message:
        if message.reply_to_message.photo:
            media_path = await message.reply_to_message.download()
        elif message.reply_to_message.video:
            media_path = await message.reply_to_message.download()
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type == 'image/gif':
            media_path = await message.reply_to_message.download()
        elif message.reply_to_message.sticker:
            # Download the sticker
            media_path = await message.reply_to_message.download()

        if media_path:
            imgbb_link = upload_media_to_imgbb(media_path)
            
            if imgbb_link:
                # Send a message with the link embedded under text using Markdown format
                text = f"Here is your media: {imgbb_link}"
                await message.reply_text(text)
            else:
                await message.reply_text("gagal mengupload media kamu.")
        else:
            await message.reply_text("Unsupported media type or no media found.")
    else:
        await message.reply_text("tolong reply photo, video, GIF, or sticker.")
      
