from pyrogram import filters
from pyrogram.types import User
from DanteUserbot import *
from DanteUserbot.core.database.premium import get_prem  # Import the get_prem function

async def get_all_users():
    """
    Mengambil semua pengguna premium dari database dan mengembalikan daftar User.
    """
    premium_user_ids = await get_prem()
    users = []
    
    for user_id in premium_user_ids:
        try:
            user = await bot.get_users(user_id)  # Mengambil data lengkap user
            users.append(User(id=user.id, username=user.username or "", first_name=user.first_name))
        except Exception:
            continue  # Lewati jika user tidak ditemukan
    
    return users


async def call_all_users():
    """
    Mengirim pesan ke semua pengguna premium yang terdaftar.
    """
    users = await get_all_users()  # Perbaikan: Tambahkan await
    for user in users:
        try:
            await bot.send_message(user.id, "🔹 Ini adalah pesan untuk semua pengguna premium.")
        except Exception as e:
            print(f"❌ Gagal mengirim pesan ke {user.id}: {e}")  # Menangani error jika ada user yang tidak bisa dikirimi pesan

