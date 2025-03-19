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
            if os.path.getsize(filepath) == 0:  # Jika file kosong, berarti sesi sudah tidak digunakan
                os.remove(filepath)

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
        print(f"[INFO] - Userbot {user_id} berhasil dijalankan.")  # Tambahkan log
    except asyncio.TimeoutError:
        print(f"[INFO] - Userbot ({user_id}) tidak merespon, mencoba restart...")
        try:
            await asyncio.sleep(5)
            await ubot_.start()
        except Exception:
            await bersihkan_userbot(user_id, tambahkan_premium=True)
            print(f"[INFO] - Userbot ({user_id}) tetap gagal, menghapus data.")
    except Exception as e:
        await bersihkan_userbot(user_id)
        print(f"⚠️ {user_id} gagal dijalankan. Error: {e}")

# Fungsi utama untuk menjalankan semua userbot
async def main():
    await hapus_session_kadaluarsa()  # Use the Python implementation instead of bash

    userbots = await get_DanteUserbots()
    tasks = [asyncio.shield(start_ubot(int(bot["name"]), bot)) for bot in userbots]

    # Start the bot client before loading plugins
    await bot.start()

    # Start userbots and other tasks
    await asyncio.gather(*tasks, loadPlugins(), expiredUserbots(), idle())

if __name__ == "__main__":
    asyncio.run(main())  # Menggunakan asyncio.run() untuk stabilitas lebih baik
