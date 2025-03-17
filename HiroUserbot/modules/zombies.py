from HiroUserbot import *
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid

__MODULE__ = "ᴢᴏᴍʙɪᴇ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴢᴏᴍʙɪᴇꜱ--**
<blockquote><b>
<b>ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}zombies</code>
<b>ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ ᴅɪɢʀᴜᴘ ᴀɴᴅᴀ.</b></blockquote>
"""

@HIRO.UBOT("zombies")
async def zombies_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    jdl = await EMO.JUDUL(client)
    try:
        chat_id = message.chat.id
        deleted_users = []
        banned_users = 0
        Tm = await message.reply(f"<b>{prs}ᴘʀᴏᴄᴄᴇsɪɴɢ...</b>")
        async for i in client.get_chat_members(chat_id):
            if i.user.is_deleted:
                deleted_users.append(i.user.id)
        if len(deleted_users) > 0:
            for deleted_user in deleted_users:
                try:
                    banned_users += 1
                    await message.chat.ban_member(deleted_user)
                except Exception:
                    pass
            await Tm.edit(f"{sks}<b>ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ {banned_users} ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ</b>")
        else:
            await Tm.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ</b>")
    except ChannelInvalid:
        await Tm.edit(f"{ggl}<b>ɢᴜɴᴀᴋᴀɴ ᴅɪ ɢʀᴜᴘ</b>")
