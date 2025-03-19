from importlib import import_module
from platform import python_version

from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from DanteUserbot import bot, ubot
from DanteUserbot.config import OWNER_ID
from DanteUserbot.core.helpers import DANTE
from DanteUserbot.modules import loadModule

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    
    # Ensure bot.me is initialized
    if bot.me is None:
        bot.me = await bot.get_me()
    
    for mod in modules:
        imported_module = import_module(f"DanteUserbot.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[🤖 @{bot.me.username}] [⚡ TELAH BERHASIL DIAKTIFKAN!]")
    TM = await bot.send_message(
        OWNER_ID,
        f"""
<b>🤖 {bot.me.mention} berhasil diaktifkan</b>

<b>📁 modules: {len(HELP_COMMANDS)}</b>
<b>📘 python: {python_version()}</b>
<b>📙 pyrogram: {__version__}</b>

<b>👤 DanteUserbot: {len(ubot._ubot)}</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🛠️ gitpull", callback_data="gitpull"),
                    InlineKeyboardButton("restart 🔁", callback_data="restart"),
                ],
            ]
        ),
    )
    
    

@DANTE.CALLBACK("0_cls")
async def _(client, callback_query):
await callback_query.message.delete()

