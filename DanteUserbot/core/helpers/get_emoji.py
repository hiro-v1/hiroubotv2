from DanteUserbot.core.function.emoji import emoji as static_emoji
from DanteUserbot.core.helpers.emoji import EMO

async def get_emoji(client, alias):
    """
    Mengambil emoji dari database (jika ada) atau menggunakan emoji statis sebagai default.
    """
    emoji_map = {
        "ping": EMO.PING,
        "mention": EMO.MENTION,
        "judul": EMO.JUDUL,
        "ubot": EMO.UBOT,
        "uptime": EMO.UPTIME,
        "proses": EMO.PROSES,
        "berhasil": EMO.BERHASIL,
        "gagal": EMO.GAGAL,
        "broadcast": EMO.BROADCAST,
        "group": EMO.BL_GROUP,
        "keterangan": EMO.BL_KETERANGAN,
        "menunggu": EMO.MENUNGGU,
        "putaran": EMO.PUTARAN,
        "afka": EMO.AEFKA,
        "alasan": EMO.ALASAN,
        "waktu": EMO.WAKTU,
        "pyrogram": EMO.PYROGRAM,
        "pytgcalls": EMO.PYTGCALS,
    }
    
    if alias in emoji_map:
        return await emoji_map[alias](client)  # Coba ambil dari database

    return static_emoji(alias)  # Jika tidak ada, gunakan emoji statis
