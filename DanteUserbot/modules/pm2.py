from pyrogram import *
from DanteUserbot.config import DEVS
from DanteUserbot import *
from DanteUserbot.core.helpers.emoji import EMO

PM_GUARD_WARNS_DB = {}
PM_GUARD_MSGS_DB = {}

DEFAULT_TEXT = """<blockquote>
<b>👋 Hey! Ada yang bisa gue bantu?</b>  

Gue adalah asisten otomatis. Tinggalin pesan aja, nanti majikan gue bakal bales kalo lagi ga sibuk. ⏳  

🚫 <i>Jangan spam ya, atau lo bakal diblokir otomatis.</i>  
</blockquote>"""

PM_WARN = """
<blockquote>
{}
⚠️ Lo udah dapet <b>{}/{}</b> peringatan. Sabar ya, jangan spam!
</blockquote>
"""

LIMIT = 5

@DANTE.UBOT("pm")
async def permitpm(client, message):
    user_id = client.me.id
    babi = await message.edit("`Processing...`")
    bacot = get_arg(message)
    if not bacot:
        return await babi.edit(f"`Gunakan Format : `{0}pmpermit on or off`.`")
    is_already = await get_var(user_id, "ENABLE_PM_GUARD")
    if bacot.lower() == "on":
        if is_already:
            return await babi.edit("`PMPermit Sudah DiHidupkan.`")
        await set_var(user_id, "ENABLE_PM_GUARD", True)
        await babi.edit("`PMPermit Berhasil DiHidupkan.`")
    elif bacot.lower() == "off":
        if not is_already:
            return await babi.edit("`PMPermit Sudah DiMatikan.`")
        await set_var(user_id, "ENABLE_PM_GUARD", False)
        await babi.edit("`PMPermit Berhasil DiMatikan.`")
    else:
        await babi.edit(f"`Gunakan Format : `{0}pmpermit on or off`.`")


@DANTE.UBOT("ok")
async def approve(client, message):
    babi = await message.edit("`Processing...`")
    chat_type = message.chat.type
    if chat_type == "me":
        return await babi.edit("`Apakah anda sudah gila ?`")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit("`Balas ke pesan pengguna, untuk disetujui.`")
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if already_apprvd:
        return await babi.edit("`Manusia ini sudah Di Setujui Untuk mengirim pesan.`")
    await add_approved_user(user_id)
    if user_id in PM_GUARD_WARNS_DB:
        PM_GUARD_WARNS_DB.pop(user_id)
        try:
            await client.delete_messages(
                chat_id=user_id, message_ids=PM_GUARD_MSGS_DB[user_id]
            )
        except BaseException:
            pass
    await babi.edit("`Baiklah, pengguna ini sudah disetujui untuk mengirim pesan.`")


@DANTE.UBOT("no")
async def disapprove(client, message):
    babi = await message.edit("`Processing...`")
    chat_type = message.chat.type
    if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit("`Balas ke pesan pengguna, untuk ditolak.`")
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if not already_apprvd:
        return await babi.edit(
            "`Manusia ini memang belum Di Setujui Untuk mengirim pesan.`"
        )
    await rm_approved_user(user_id)
    await babi.edit("`Baiklah, pengguna ini ditolak untuk mengirim pesan.`")


@DANTE.UBOT("setpm")
async def set_msg(client, message):
    babi = await message.edit("`Processing...`")
    user_id = client.me.id
    r_msg = message.reply_to_message
    args_txt = get_arg(message)
    if r_msg:
        if r_msg.text:
            pm_txt = r_msg.text
        else:
            return await babi.edit(
                "`Silakan balas ke pesan untuk dijadikan teks PMPermit !`"
            )
    elif args_txt:
        pm_txt = args_txt
    else:
        return await babi.edit(
            "`Silakan balas ke pesan atau berikan pesan untuk dijadikan teks PMPermit !\n`Contoh :` {0}setmsg Halo saya anuan`"
        )
    await set_var(user_id, "CUSTOM_PM_TEXT", pm_txt)
    await babi.edit(f"`Pesan PMPemit berhasil diatur menjadi : `{pm_txt}`.`")


@DANTE.UBOT("setlimit")
async def set_limit(client, message):
    babi = await message.edit("`Processing...`")
    user_id = client.me.id
    args_txt = get_arg(message)
    if args_txt:
        if args_txt.isnumeric():
            pm_warns = int(args_txt)
        else:
            return await babi.edit("`Silakan berikan untuk angka limit !`")
    else:
        return await babi.edit(
            f"`Silakan berikan pesan untuk dijadikan angka limit !\n`Contoh :` {0}setlimit 5`"
        )
    await set_var(user_id, "CUSTOM_PM_WARNS_LIMIT", pm_warns)
    await babi.edit(f"`Pesan Limit berhasil diatur menjadi : `{args_txt}`.`")


@ubot.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def handle_pmpermit(client, message):
    user_id = client.me.id
    siapa = message.from_user.id
    chat_id = message.chat.id

    # Cek apakah fitur PM-Permit aktif
    is_pm_guard_enabled = await get_var(user_id, "ENABLE_PM_GUARD")
    if not is_pm_guard_enabled:
        return

    in_user = message.from_user
    is_approved = await check_user_approved(in_user.id)
    if is_approved:
        return

    # Blokir pengguna mencurigakan (Fake/Scam)
    if in_user.is_fake or in_user.is_scam:
        await message.reply("⚠️ Sepertinya Anda mencurigakan...", parse_mode="html")
        return await client.block_user(in_user.id)

    # Ambil teks PM-Permit Custom
    getc_pm_txt = await get_var(user_id, "CUSTOM_PM_TEXT")
    getc_pm_warns = await get_var(user_id, "CUSTOM_PM_WARNS_LIMIT")

    # Jika ada custom PM-Permit, gunakan, jika tidak pakai DEFAULT_TEXT
    custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT

    # Hapus pesan sebelumnya jika ada
    if chat_id in PM_GUARD_MSGS_DB:
        try:
            await client.delete_messages(chat_id, PM_GUARD_MSGS_DB[chat_id])
        except Exception as e:
            print(f"⚠️ Gagal menghapus pesan lama: {str(e)}")

    # ✅ Mengirim pesan dengan emoji premium jika pengguna Telegram Premium
    rplied_msg = await message.reply(
        f"{custom_pm_txt}",
        parse_mode="html",  # 🔹 Pakai HTML agar emoji premium bisa muncul
    )

    # Simpan pesan agar bisa dihapus jika ada pesan baru
    PM_GUARD_MSGS_DB[chat_id] = rplied_msg.id

async def delete_old_message(message, msg_id):
    try:
        await message._client.delete_messages(message.chat.id, msg_id)
    except:
        pass

__MODULE__ = "ᴘᴍᴘᴇʀᴍɪᴛ"
__HELP__ = """<blockquote><b>
   Bantuan untuk PM-Permit

command: {0}pm [on/off]
   mengaktifkan atau menonaktifkan pm permit
   
command: {0}ok
   mengizinkan seseorang untuk pm anda

command: {0}no
   menolak seseorang untuk pm anda

command: {0}setpm
   query: replay text
   mengatur pesan custom pada pm_permit

command: {0}setlimit
   query: angka
   mengatur batas peringatan pada pm_permit

contoh menggunakan warning 
   command: setlimit 5</b></blockquote>
"""
