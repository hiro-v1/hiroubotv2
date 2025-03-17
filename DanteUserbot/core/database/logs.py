from DanteUserbot.core.database import db

LOGGING_STATUS = "logging_status"
NOLOG_USERS = "nolog_users"
LOG_OPTION = "log_option"

async def enable_logging(user_id: int):
    """Aktifkan logging untuk pengguna tertentu."""
    await db.set(LOGGING_STATUS, user_id, True)

async def disable_logging(user_id: int):
    """Nonaktifkan logging untuk pengguna tertentu."""
    await db.set(LOGGING_STATUS, user_id, False)

async def is_logging_enabled(user_id: int) -> bool:
    """Cek apakah logging aktif untuk pengguna tertentu."""
    return await db.get(LOGGING_STATUS, user_id, default=False)

async def add_nolog_user(owner_id: int, user_id: int):
    """Tambahkan pengguna ke daftar yang diabaikan (`nolog`)."""
    nolog_list = await db.get(NOLOG_USERS, owner_id, default=[])
    if user_id not in nolog_list:
        nolog_list.append(user_id)
        await db.set(NOLOG_USERS, owner_id, nolog_list)

async def remove_nolog_user(owner_id: int, user_id: int):
    """Hapus pengguna dari daftar `nolog`."""
    nolog_list = await db.get(NOLOG_USERS, owner_id, default=[])
    if user_id in nolog_list:
        nolog_list.remove(user_id)
        await db.set(NOLOG_USERS, owner_id, nolog_list)

async def get_nolog_users(owner_id: int) -> list:
    """Ambil daftar pengguna yang masuk daftar `nolog`."""
    return await db.get(NOLOG_USERS, owner_id, default=[])

async def set_log_option(user_id: int, option: str):
    """Tentukan opsi logging: 'all', 'group', atau 'chat'."""
    valid_options = ["all", "group", "chat"]
    if option in valid_options:
        await db.set(LOG_OPTION, user_id, option)

async def get_log_option(user_id: int) -> str:
    """Ambil opsi logging yang dipilih pengguna."""
    return await db.get(LOG_OPTION, user_id, default="all")
