from DanteUserbot import *
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DanteUserbot.core.helpers.client import bot, OWNER_ID, MSG, DANTE

SUPPORT = []
SUPPORT_LOCK = asyncio.Lock()  # Lock untuk mencegah race condition

async def support_callback(client, callback_query):
    """ Menangani permintaan dukungan dari pengguna """
    user_id = callback_query.from_user.id
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"

    # Pastikan user valid
    get = await bot.get_users(user_id)
    if not get:
        return await callback_query.message.edit("⚠️ Pengguna tidak ditemukan.")

    async with SUPPORT_LOCK:  # Gunakan lock untuk menghindari duplikasi
        if user_id in SUPPORT:
            return await callback_query.answer("❗ Anda sudah dalam antrian support.", show_alert=True)
        SUPPORT.append(user_id)

    await callback_query.message.delete()

    try:
        button = [[InlineKeyboardButton("🔙 Kembali", callback_data=f"home {user_id}")]]
        pesan = await bot.ask(
            user_id,
            f"<b>📝 Silahkan kirim pertanyaan Anda: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError:
        async with SUPPORT_LOCK:
            SUPPORT.remove(user_id)
        return await bot.send_message(user_id, "⏳ Waktu habis, permintaan dibatalkan.")

    # Kirim pertanyaan ke OWNER
    text = f"📩 <b>Pertanyaan dari:</b> {full_name}"
    buttons = [
        [
            InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("💬 Jawab", callback_data=f"jawab_pesan {user_id}"),
        ]
    ]
    try:
        await pesan.copy(OWNER_ID, reply_markup=InlineKeyboardMarkup(buttons))
        async with SUPPORT_LOCK:
            SUPPORT.remove(user_id)
        return await bot.send_message(user_id, "✅ Pertanyaan berhasil dikirim.")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return await bot.send_message(user_id, "❌ Gagal mengirim pertanyaan.")

async def jawab_pesan_callback(client, callback_query):
    """ Owner membalas pesan pengguna """
    owner_id = callback_query.from_user.id
    user_id = int(callback_query.data.split()[1])

    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(owner_id)

    if not get:
        return await callback_query.message.edit("⚠️ Pengguna tidak ditemukan.")

    async with SUPPORT_LOCK:
        SUPPORT.append(owner_id)

    try:
        button = [[InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {owner_id}")]]
        pesan = await bot.ask(
            owner_id,
            f"<b>📝 Silahkan kirim balasan Anda: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        async with SUPPORT_LOCK:
            SUPPORT.remove(owner_id)
        return await bot.send_message(owner_id, "⏳ Waktu habis, permintaan dibatalkan.")

    text = f"📩 <b>Balasan dari:</b> {full_name}"
    buttons = [[InlineKeyboardButton("💬 Balas", callback_data=f"jawab_pesan {user_id}")]]

    try:
        await pesan.copy(user_id, reply_markup=InlineKeyboardMarkup(buttons))
        async with SUPPORT_LOCK:
            SUPPORT.remove(owner_id)
        return await bot.send_message(owner_id, "✅ Pesan balasan berhasil dikirim.")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return await bot.send_message(owner_id, "❌ Gagal mengirim balasan.")

async def profil_callback(client, callback_query):
    """ Menampilkan profil pengguna """
    user_id = int(callback_query.data.split()[1])

    get = await bot.get_users(user_id)
    if not get:
        return await callback_query.message.edit("⚠️ Pengguna tidak ditemukan.")

    full_name = f"{get.first_name} {get.last_name or ''}".strip()
    username = f"@{get.username}" if get.username else "🚫 Tidak ada username"

    msg = (
        f"👤 <b>Profil Pengguna:</b>\n"
        f"📌 <b>Nama:</b> {full_name}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{get.id}</code>\n"
        f"🤖 <b>Bot:</b> {bot.me.mention}"
    )

    buttons = [[InlineKeyboardButton(f"📩 Kirim Pesan", url=f"tg://openmessage?user_id={get.id}")]]
    
    return await callback_query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

async def batal_callback(client, callback_query):
    """ Membatalkan permintaan support """
    user_id = int(callback_query.data.split()[1])

    async with SUPPORT_LOCK:
        if user_id in SUPPORT:
            SUPPORT.remove(user_id)
        else:
            return await callback_query.answer("❌ Tidak ada permintaan yang aktif.", show_alert=True)

    await callback_query.message.delete()
    return await bot.send_message(user_id, "✅ Permintaan support telah dibatalkan.")

# Handler Callback Query
@DANTE.CALLBACK("support")
async def support_callback(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.edit_message_text(
        f"📩 Halo {callback_query.from_user.first_name},\n\n"
        f"Silakan kirim pertanyaan Anda, tim kami akan segera membantu Anda.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Kembali", callback_data=f"home {user_id}")]]
        ),
    )

@DANTE.CALLBACK("^jawab_pesan")
async def _(client, callback_query):
    await jawab_pesan_callback(client, callback_query)

@DANTE.CALLBACK("^profil")
async def _(client, callback_query):
    await profil_callback(client, callback_query)

@DANTE.CALLBACK("^batal")
async def _(client, callback_query):
    await batal_callback(client, callback_query)

@DANTE.CALLBACK("hubungi_owner")
async def _(client, callback_query):
    buttons = [[InlineKeyboardButton("🔙 Kembali", callback_data="start")]]
    await callback_query.edit_message_text(
        f"📩 Halo {callback_query.from_user.first_name},\n\n"
        f"Silakan hubungi owner untuk bantuan lebih lanjut.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
