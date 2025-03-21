import asyncio
import os
from pyrogram import idle
from DanteUserbot import *
from pyrogram import Client

# Fungsi untuk menghapus sesi yang kadaluarsa
async def hapus_session_kadaluarsa():
    """Hapus hanya sesi yang tidak digunakan"""
    for filename in os.listdir():
        if filename.endswith(".session"):
            filepath = os.path.join(os.getcwd(), filename)
            os.remove(filepath)  # Remove all SQLite session files

# Fungsi untuk membersihkan userbot yang gagal atau tidak merespons
async def bersihkan_userbot(user_id, tambahkan_premium=False):
    await remove_ubot(user_id)
    await rm_all(user_id)
    await remove_all_vars(user_id)
    await rem_pref(user_id)
    await rem_expired_date(user_id)

    for chat_id in await get_chat(user_id):
        await remove_chat(user_id, chat_id)

    if tambahkan_premium:
        await add_prem(user_id)
        await sending_user(user_id)

    # Kirim notifikasi ke OWNER jika tersedia
    if OWNER_ID:
        await bot.send_message(
            OWNER_ID, f"❌ Userbot {user_id} telah dihapus dari sistem."
        )

    print(f"[INFO] - Userbot ({user_id}) berhasil dibersihkan.")

# Fungsi untuk memulai userbot
async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        print(f"[INFO] - Userbot {user_id} berhasil dijalankan.")
    except asyncio.TimeoutError:
        print(f"[INFO] - Userbot ({user_id}) tidak merespon, mencoba restart...")
        await remove_ubot(user_id)
        await add_prem(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await remove_all_vars(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        await sending_user(user_id)
    except Exception as e:
        print(f"⚠️ {user_id} gagal dijalankan. Error: {e}")
        await remove_ubot(user_id)
        await rm_all(user_id)
        await remove_all_vars(user_id)
        await rem_pref(user_id)
        await rem_expired_date(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)

# Fungsi utama untuk menjalankan semua userbot
async def main():
    print("[LOG] Memulai bot...")
    await bot.start()
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_DanteUserbots()
    ]
    await asyncio.gather(*tasks, idle())

if __name__ == "__main__":
    asyncio.run(main())
