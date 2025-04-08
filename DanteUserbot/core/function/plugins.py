from importlib import import_module
from platform import python_version
from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DanteUserbot import bot, ubot
from DanteUserbot.config import OWNER_ID
from DanteUserbot.modules import loadModule
from DanteUserbot.core.helpers.text import MSG
from DanteUserbot.core.helpers.client import DANTE 

HELP_COMMANDS = {}

async def loadPlugins():
    """Memuat semua modul dan mengirim pesan saat bot diaktifkan."""
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"DanteUserbot.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[🤖 @{bot.me.username}] [⚡ TELAH BERHASIL DIAKTIFKAN!]")
    await bot.send_message(
        OWNER_ID,
        MSG.PLUGINS_ACTIVATED(bot, ubot, python_version(), __version__, len(HELP_COMMANDS)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🛠️ GitPull", callback_data="cb_gitpull"),
                    InlineKeyboardButton("🔁 Restart", callback_data="cb_restart"),
                ],
            ]
        ),
    )

@DANTE.CALLBACK("0_cls")
async def close_message(client, callback_query):
    """Menghapus pesan callback."""
    await callback_query.message.delete()

