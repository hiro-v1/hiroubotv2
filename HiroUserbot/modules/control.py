from HiroUserbot import *

__MODULE__ = "ᴘʀᴇғɪx"
__HELP__ = f"""
**--bantuan untuk merubah tampilan prefix--**
<blockquote><b>
  <b>• perintah:</b> <code>{PREFIX[0]}setprefix</code> [simbol prefix]
  <b>• kegunaan:</b> untuk merubah tampilan prefix command 

none: hanya untuk pengguna akun telegram premium yang bisa menggunakan emoji premium!

  <b>• perintah:</b> <code>{PREFIX[0]}setemoji</code> [query] [valeu]
  <b>• query: </b>
       <b>proses</b>
       <b>gagal</b>
       <b>berhasil</b>
  <b>• untuk mengubah tampilan emoji pada command</b>

</b></blockquote>"""

@HIRO.UBOT("setprefix")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.reply(f"{prs}<b>ᴍᴇᴍᴘʀᴏsᴇs</b>", quote=True)
    if len(message.command) < 2:
        return await Tm.edit(f"{ggl}<code>{message.text}</code> sɪᴍʙᴏʟ ᴘʀᴇғɪx")
    else:
        ub_prefix = []
        for prefix in message.command[1:]:
            if prefix.lower() == "none":
                ub_prefix.append("")
            else:
                ub_prefix.append(prefix)
        try:
            client.set_prefix(message.from_user.id, ub_prefix)
            await set_pref(message.from_user.id, ub_prefix)
            parsed_prefix = " ".join(f"<code>{prefix}</code>" for prefix in ub_prefix)
            return await Tm.edit(f"{sks}<b>ᴘʀᴇғɪx ᴛᴇʟᴀʜ ᴅɪᴜʙᴀʜ ᴋᴇ : {parsed_prefix}</b>")
        except Exception as error:
            return await Tm.edit(str(error))



@HIRO.UBOT("setemoji")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    try:
        msg = await message.reply(f"{prs}<b>ᴍᴇᴍᴘʀᴏsᴇs</b>...", quote=True)

        if not client.me.is_premium:
            return await msg.edit(
                "<b>ʙᴇʟɪ ᴛᴇʟᴇᴘʀᴇᴍ ᴅᴜʟᴜ ᴀɴᴊɴɢ !</b>"
            )

        if len(message.command) < 3:
            return await msg.edit(f"{ggl}<b>ᴛᴏʟᴏɴɢ ᴍᴀsᴜᴋᴋᴀɴ ǫᴜᴇʀʏ ᴅᴀɴ ᴠᴀʟᴇᴜ ɴʏᴀ</b>")

        query_mapping = {"proses": "EMOJI_PROSES", "berhasil": "EMOJI_BERHASIL", "gagal": "EMOJI_GAGAL"}
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = None
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break

            if emoji_id:
                await set_vars(client.me.id, query_var, emoji_id)
                await msg.edit(
                    f"{sks}<code>{query_var}</code> <b>ʙᴇʀʜᴀsɪʟ ᴅɪ sᴇᴛᴛɪɴɢ ᴋᴇ:</b> <emoji id={emoji_id}>{value}</emoji>"
                )
            else:
                await msg.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴇᴍᴏᴊɪ ᴘʀᴇᴍɪᴜᴍ</b>")
        else:
            await msg.edit(f"{ggl}<b>ᴍᴀᴘᴘɪɴɢ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")

    except Exception as error:
        await msg.edit(str(error))
