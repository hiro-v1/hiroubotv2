__MODULE__ = "ᴀғᴋ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀꜰᴋ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}afk</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴀꜰᴋ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}unafk</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀꜰᴋ</b></blockquote>
  """
from time import time
import os
from DanteUserbot import *
from pyrogram.enums import ChatType
from pyrogram.types import Message
from DanteUserbot.core.helpers.emoji import EMO
from DanteUserbot.core.function.emoji import emoji

class awayFromKeyboard:
    def __init__(self, client, message, reason="", emoji_alias=""):
        self.client = client
        self.message = message
        self.reason = reason
        self.emoji_alias = emoji_alias

    async def set_afk(self):
        db_afk = {"time": time(), "reason": self.reason}
        emoji_afk = await EMO.AEFKA(self.client)
        custom_emoji = emoji(self.emoji_alias) if self.emoji_alias else emoji_afk
        msg_afk = (
            f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ {custom_emoji}\n ╰ ᴀʟᴀsᴀɴ: {self.reason}</b>"
            if self.reason
            else f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ {custom_emoji}</b>"
        )
        await set_vars(self.client.me.id, "AFK", db_afk)
        await self.message.reply(msg_afk, disable_web_page_preview=True)
        return await self.message.delete()

    async def get_afk(self):
        vars = await get_vars(self.client.me.id, "AFK")
        if vars:
            afk_time = vars.get("time")
            afk_reason = vars.get("reason")
            afk_runtime = await get_time(time() - afk_time)
            emoji_afk = await EMO.AEFKA(self.client)
            custom_emoji = emoji(self.emoji_alias) if self.emoji_alias else emoji_afk
            afk_text = (
                f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ {custom_emoji}\n ├ ᴡᴀᴋᴛᴜ: {afk_runtime}\n ╰ ᴀʟᴀsᴀɴ: {afk_reason}</b>"
                if afk_reason
                else f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ {custom_emoji}\n ╰ ᴡᴀᴋᴛᴜ: {afk_runtime}</b>"
            )
            return await self.message.reply(afk_text, disable_web_page_preview=True)

    async def unset_afk(self):
        vars = await get_vars(self.client.me.id, "AFK")
        if vars:
            afk_time = vars.get("time")
            afk_runtime = await get_time(time() - afk_time)
            emoji_afk = await EMO.AEFKA(self.client)
            custom_emoji = emoji(self.emoji_alias) if self.emoji_alias else emoji_afk
            afk_text = f"<b>❏ ᴋᴇᴍʙᴀʟɪ ᴏɴʟɪɴᴇ {custom_emoji}\n ╰ ᴀғᴋ sᴇʟᴀᴍᴀ: {afk_runtime}</b>"
            await self.message.reply(afk_text)
            await self.message.delete()
            return await remove_vars(self.client.me.id, "AFK")


@DANTE.UBOT("afk")
async def _(client, message):
    args = message.text.split(" ", 2)
    reason = args[1] if len(args) > 1 else ""
    emoji_alias = args[2] if len(args) > 2 else ""
    afk_handler = awayFromKeyboard(client, message, reason, emoji_alias)
    await afk_handler.set_afk()

@DANTE.AFK(True)
async def _(client, message):
    afk_handler = awayFromKeyboard(client, message)
    await afk_handler.get_afk()

@DANTE.UBOT("unafk")
async def _(client, message):
    afk_handler = awayFromKeyboard(client, message)
    return await afk_handler.unset_afk()
