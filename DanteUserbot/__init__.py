import uvloop

uvloop.install()

import logging
import os
import re

from pyrogram import Client, filters
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from pytgcalls import GroupCallFactory
from pytgcalls.group_call_type import GroupCallType
from pytgcalls.mtproto_client_type import MTProtoClientType
from DanteUserbot.config import *

class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for X in ["OSError", "TimeoutError"]:
            if X in record.getMessage():
                os.system(f"kill -9 {os.getpid()} && python3 -m DanteUserbot")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="Dante UBot")

    async def start(self):
        await super().start()
        if not self.me:
            self.me = await self.get_me()  # Pastikan bot.me diinisialisasi
        print(f"[INFO] Bot {self.me.username} berhasil dijalankan.")

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def get_text(self, m):
        if m.reply_to_message:
            if len(m.command) < 2:
                text = m.reply_to_message.text or m.reply_to_message.caption
            else:
                text = (
                    (m.reply_to_message.text or m.reply_to_message.caption)
                    + "\n\n"
                    + m.text.split(None, 1)[1]
                )
        else:
            if len(m.command) < 2:
                text = ""
            else:
                text = m.text.split(None, 1)[1]
        return text
        
    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="Dante UBot")
        self.group_call_factory = GroupCallFactory(self, MTProtoClientType.PYROGRAM)
        self.call_py = self.group_call_factory.get(GroupCallType.RAW)
        self.device_model = "Dante UBot"
        
    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def get_chats_dialog(self, q):
        chat_types = {
            "grup": [ChatType.GROUP, ChatType.SUPERGROUP],
            "all": [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.PRIVATE,
            ],
            "bot": [ChatType.BOT],
            "usbot": [ChatType.PRIVATE, ChatType.BOT],
            "user": [ChatType.PRIVATE],
            "gban": [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ],
            "ch": [ChatType.CHANNEL],
        }
        return [
            dialog.chat.id
            async for dialog in self.get_dialogs()
            if dialog.chat.type in chat_types.get(q, [])
        ]

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix
    
    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    async def start(self):
        await super().start()
        if not self.me:
            self.me = await self.get_me()  # Pastikan ubot.me diinisialisasi
        if hasattr(self, "call_py") and self.call_py:
            try:
                await self.call_py.start(group=None)  # Mulai panggilan grup jika ada
            except Exception as e:
                print(f"⚠️ Gagal memulai panggilan grup: {e}")
        handler = await get_pref(self.me.id)
        self._prefix[self.me.id] = handler if handler else ["."]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"
        print(f"[INFO] Userbot {self.me.id} berhasil dijalankan.")

bot = Bot(
    name="bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

ubot = Ubot(name="ubot")

from DanteUserbot.core.database import *
from DanteUserbot.core.function import *
from DanteUserbot.core.helpers import *
