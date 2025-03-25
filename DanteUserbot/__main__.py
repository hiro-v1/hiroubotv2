import asyncio
import os
from pyrogram import idle
from DanteUserbot import bot, get_DanteUserbots, Ubot
from DanteUserbot.core.database.DanteUserbot import remove_ubot  # Tambahkan impor ini
from DanteUserbot.core.database import rm_all, remove_all_vars, rem_pref, rem_expired_date, get_chat, remove_chat

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
        await bersihkan_userbot(user_id, tambahkan_premium=True)
        await ubot_.start()
        print(f"[INFO] Userbot {user_id} berhasil dijalankan.")
    except Exception as e:
        print(f"⚠️ {user_id} gagal dijalankan. Error: {e}")
        await bersihkan_userbot(user_id)

# Fungsi utama untuk menjalankan semua userbot
async def main():
    print("[LOG] Memulai bot...")
    try:
        await bot.start()
        print(f"[INFO] Bot {bot.me.username} berhasil dijalankan.")
    except Exception as e:
        print(f"⚠️ Gagal menjalankan bot: {e}")
        return

    tasks = []
    for _ubot in await get_DanteUserbots():
        user_id = int(_ubot["name"])
        tasks.append(asyncio.create_task(start_ubot(user_id, _ubot)))

    if tasks:
        await asyncio.gather(*tasks)
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
