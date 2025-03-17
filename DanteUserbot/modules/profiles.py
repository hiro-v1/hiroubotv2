from DanteUserbot import *
from DanteUserbot.core.helpers.emoji import EMO

__MODULE__ = 'ᴘʀᴏғɪʟ'
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘʀᴏꜰɪʟᴇ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴇᴛʙɪᴏ</code> [ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ʙɪᴏ ᴀɴᴅᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴇᴛɴᴀᴍᴇ</code> [ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɴᴀᴍᴀ ᴀɴᴅᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴇᴛᴘᴘ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴅᴇʟᴘᴘ</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜꜱ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ʜɪᴅᴘᴘ</code> [ᴏɴ/ᴏꜰꜰ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴʏᴇᴍʙᴜɴʏɪᴋᴀɴ/ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ʙʟᴏᴄᴋ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴜɴʙʟᴏᴄᴋ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴋᴀ ʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ
</b></blockquote>"""

import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

@DANTE.UBOT('setbio')
async def set_bio(client: Client, message: Message) -> None:
    """Set the bio of the user."""
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    if len(message.command) == 1:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan teks untuk ditetapkan sebagai bio.')
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(f'{await EMO.BERHASIL(client)} berhasil mengubah bio menjadi <code>{bio}</code>')
        except Exception as e:
            await tex.edit(f'{await EMO.GAGAL(client)} ERROR: <code>{e}</code>')
    else:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan teks untuk ditetapkan sebagai bio.')

@DANTE.UBOT('setname')
async def set_name(client: Client, message: Message) -> None:
    """Set the name of the user."""
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    if len(message.command) == 1:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan teks untuk ditetapkan sebagai nama anda.')
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(f'{await EMO.BERHASIL(client)} berhasil mengubah nama menjadi <code>{name}</code>')
        except Exception as e:
            await tex.edit(f'{await EMO.GAGAL(client)} ERROR: <code>{e}</code>')
    else:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan teks untuk ditetapkan sebagai nama anda.')

@DANTE.UBOT('block')
async def block_user(client: Client, message: Message) -> None:
    """Block a user."""
    user_id = await extract_user(message)
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    if not user_id:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan nama pengguna untuk diblokir.')
    if user_id == client.me.id:
        return await tex.edit(f'{await EMO.BERHASIL(client)} ok done.')
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f'{await EMO.BERHASIL(client)} berhasil diblokir {umention}')

@DANTE.UBOT('unblock')
async def unblock_user(client: Client, message: Message) -> None:
    """Unblock a user."""
    user_id = await extract_user(message)
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    if not user_id:
        return await tex.edit(f'{await EMO.GAGAL(client)} berikan nama pengguna atau balas pesan untuk membuka blokir.')
    if user_id == client.me.id:
        return await tex.edit(f'{await EMO.BERHASIL(client)} ok done.')
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f'{await EMO.BERHASIL(client)} berhasil dibebaskan {umention}')

@DANTE.UBOT('setpp')
async def set_pp(client: Client, message: Message):
    """Mengubah foto profil dengan membalas gambar."""
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await tex.edit(f'{await EMO.GAGAL(client)} Harap balas gambar untuk dijadikan foto profil!')

    photo = await message.reply_to_message.download()
    try:
        await client.set_profile_photo(photo=photo)
        await tex.edit(f'{await EMO.BERHASIL(client)} Foto profil berhasil diubah!')
        os.remove(photo)
    except Exception as e:
        await tex.edit(f'{await EMO.GAGAL(client)} Gagal mengubah foto profil:\n<code>{e}</code>', parse_mode="html")

@DANTE.UBOT('delpp')
async def del_pp(client: Client, message: Message):
    """Menghapus foto profil."""
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')

    photos = await client.get_chat_photos("me")
    if not photos:
        return await tex.edit(f'{await EMO.GAGAL(client)} Anda tidak memiliki foto profil!')

    try:
        await client.delete_profile_photos(photos[0].file_id)
        await tex.edit(f'{await EMO.BERHASIL(client)} Foto profil berhasil dihapus!')
    except Exception as e:
        await tex.edit(f'{await EMO.GAGAL(client)} Gagal menghapus foto profil:\n<code>{e}</code>', parse_mode="html")

@DANTE.UBOT('hidpp')
async def hide_pp(client: Client, message: Message):
    """Menyembunyikan atau menampilkan foto profil sesuai pengaturan Telegram."""
    tex = await message.reply(f'{await EMO.PROSES(client)} ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .')
    
    if len(message.command) < 2:
        return await tex.edit(f'{await EMO.GAGAL(client)} Gunakan perintah: <code>hidpp on</code> atau <code>hidpp off</code>', parse_mode="html")

    mode = message.command[1].lower()

    if mode == "on":
        try:
            await client.update_settings(profile_photo_visibility="nobody")
            await tex.edit(f'{await EMO.BERHASIL(client)} Foto profil disembunyikan!')
        except Exception as e:
            await tex.edit(f'{await EMO.GAGAL(client)} Gagal menyembunyikan foto profil:\n<code>{e}</code>', parse_mode="html")
    elif mode == "off":
        try:
            await client.update_settings(profile_photo_visibility="everyone")
            await tex.edit(f'{await EMO.BERHASIL(client)} Foto profil ditampilkan ke semua orang!')
        except Exception as e:
            await tex.edit(f'{await EMO.GAGAL(client)} Gagal menampilkan foto profil:\n<code>{e}</code>', parse_mode="html")
    else:
        await tex.edit(f'{await EMO.GAGAL(client)} Gunakan perintah: <code>hidpp on</code> atau <code>hidpp off</code>', parse_mode="html")
