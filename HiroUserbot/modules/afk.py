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
from HiroUserbot import *

class awayFromKeyboard:
    def __init__(self, client, message, reason=""):
        self.client = client
        self.message = message
        self.reason = reason

    async def set_afk(self):
        db_afk = {"time": time(), "reason": self.reason}
        msg_afk = (
            f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ\n ╰ ᴀʟᴀsᴀɴ: {self.reason}</b>"
            if self.reason
            else "<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ</b>"
        )
        await set_vars(self.client.me.id, "AFK", db_afk)
        await self.message.reply(msg_afk, disable_web_page_preview=True)
        return await message.delete()

    async def get_afk(self):
      vars = await get_vars(self.client.me.id, "AFK")
      if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        afk_text = (
          f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ\n ├ ᴡᴀᴋᴛᴜ: {afk_runtime}\n ╰ ᴀʟᴀsᴀɴ: {afk_reason}</b>"
          if afk_reason
          else f"<b>❏ sᴇᴅᴀɴɢ ᴀғᴋ\n ╰ ᴡᴀᴋᴛᴜ: {afk_runtime}</b>"
        )
        return await self.message.reply(afk_text, disable_web_page_preview=True)
      
    async def unset_afk(self):
        vars = await get_vars(self.client.me.id, "AFK")
        if vars:
            afk_time = vars.get("time")
            afk_runtime = await get_time(time() - afk_time)
            afk_text = f"<b>❏ ᴋᴇᴍʙᴀʟɪ ᴏɴʟɪɴᴇ\n ╰ ᴀғᴋ sᴇʟᴀᴍᴀ: {afk_runtime}"
            await self.message.reply(afk_text)
            await self.message.delete(afk_text)
            return await remove_vars(self.client.me.id, "AFK")


@HIRO.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    afk_handler = awayFromKeyboard(client, message, reason)
    await afk_handler.set_afk()


@HIRO.AFK(True)
async def _(client, message):
    afk_handler = awayFromKeyboard(client, message)
    await afk_handler.get_afk()


@HIRO.UBOT("unafk")
async def _(client, message):
    afk_handler = awayFromKeyboard(client, message)
    return await afk_handler.unset_afk()
