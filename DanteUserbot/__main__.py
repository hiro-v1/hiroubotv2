import asyncio
import os
import logging
from pyrogram import idle
from DanteUserbot import *

# Konfigurasi logging
logging.basicConfig(
    format="[%(levelname)s] - %(name)s - %(message)s",
    level=logging.INFO,  # Bisa diubah ke DEBUG untuk detail lebih banyak
)
logger = logging.getLogger(__name__)

# Fungsi untuk menghapus sesi yang kadaluarsa
async def hapus_session_kadaluarsa():
    """Hapus hanya sesi yang tidak digunakan"""
    for filename in os.listdir():
        if filename.endswith(".session"):
            filepath = os.path.join(os.getcwd(), filename)
            if os.path.getsize(filepath) == 0:  # Jika file kosong, berarti sesi sudah tidak digunakan
                os.remove(filepath)
                logger.info(f"🔄 Menghapus sesi kadaluarsa: {filename}")

# Fungsi untuk membersihkan userbot yang gagal atau tidak merespons
async def bersihkan_userbot(user_id, tambahkan_premium=False):
    """Membersihkan data userbot jika gagal dijalankan"""
    logger.warning(f"⚠️ Userbot {user_id} mengalami masalah. Menghapus data...")

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

    if OWNER_ID:
        await bot.send_message(
            OWNER_ID, f"❌ Userbot {user_id} telah dihapus dari sistem."
        )

    logger.info(f"✅ Userbot {user_id} berhasil dibersihkan.")

# Fungsi untuk memulai userbot
async def start_ubot(user_id, _ubot):
    """Memulai userbot dan menangani error jika terjadi"""
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        logger.info(f"🚀 Userbot {user_id} berhasil dijalankan.")
    except asyncio.TimeoutError:
        logger.warning(f"⏳ Userbot ({user_id}) tidak merespon, mencoba restart...")
        try:
            await asyncio.sleep(5)
            await ubot_.start()
        except Exception:
            await bersihkan_userbot(user_id, tambahkan_premium=True)
            logger.error(f"❌ Userbot ({user_id}) tetap gagal, menghapus data.")
    except Exception as e:
        await bersihkan_userbot(user_id)
        logger.error(f"❌ Userbot {user_id} gagal dijalankan. Error: {e}")

# Fungsi utama untuk menjalankan semua userbot
async def main():
    logger.info("🚀 Memulai sistem DanteUserbot...")
    await hapus_session_kadaluarsa()

    userbots = await get_DanteUserbots()
    tasks = [asyncio.create_task(start_ubot(int(bot["name"]), bot)) for bot in userbots]

    # Mulai bot utama dan userbot secara paralel
    await asyncio.gather(*tasks, bot.start(), loadPlugins(), expiredUserbots(), idle())

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Menggunakan asyncio.run() untuk stabilitas lebih baik
    except KeyboardInterrupt:
        logger.info("❌ Bot dihentikan oleh pengguna.")
