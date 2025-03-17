import uvloop
import logging
import os
import re

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from pytgcalls.types import Update as PyTgCallsUpdate
from pytgcalls.types import GroupCallParticipant
from DanteUserbot.config import *
from aiohttp import ClientSession

# Mempercepat event loop dengan uvloop
uvloop.install()

# Logger untuk menangani error dan logging bot
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
    """Kelas utama untuk mengelola bot"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="hiro UBot")

    def on_message(self, filters=None, group=-1):
        """Dekorator untuk menangani pesan masuk"""
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def get_text(self, m):
        """Mengambil teks dari pesan"""
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
        """Dekorator untuk menangani tombol inline callback"""
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func
        return decorator

    async def start(self):
        """Memulai bot dengan aman"""
        await super().start()

class Ubot(Client):
    """Kelas utama untuk userbot (Ubot) dengan dukungan panggilan suara/video"""

    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="Dante UBot")
        self.call_py = GroupCallFactory(self).get_group_call()  # Perbaikan di sini
        self.device_model = "Dante UBot"
        
    def on_message(self, filters=None, group=-1):
        """Dekorator untuk menangani pesan masuk"""
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def pytgcalls_decorator(self):
        """Dekorator untuk menangani event PyTgCalls"""
        def decorator(func):
            for ub in self._ubot:
                if func.__name__ == "kicked_handler":
                    ub.call_py.on_update(
                        PyTgCallsUpdate(
                            GroupCallParticipant.Status.KICKED | GroupCallParticipant.Status.LEFT_GROUP,
                        )
                    )(func)
                elif func.__name__ == "stream_end_handler":
                    ub.call_py.on_update(PyTgCallsUpdate.stream_end)(func)
                elif func.__name__ == "participant_handler":
                    ub.call_py.on_update(
                        PyTgCallsUpdate(
                            GroupCallParticipant.Action.JOINED,
                        )
                    )(func)
                else:
                    ub.call_py.on_update()(func)
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

    def get_arg(self, m):
        if m.reply_to_message and len(m.command) < 2:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
            return msg
        elif len(m.command) > 1:
            return " ".join(m.command[1:])
        else:
            return ""
            
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
        
    def set_prefix(self, user_id, prefix):
        """Mengatur prefix khusus untuk user tertentu."""
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        """Mengambil prefix user, default ke `.` jika tidak diatur."""
        return self._prefix.get(user_id, ["."])

    def cmd_prefix(self, cmd):
        """Filter untuk menangani command dengan prefix yang fleksibel."""
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = await self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix):]  # Hilangkan prefix dari teks

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True  # Jika ditemukan command yang cocok, kembalikan True

                return False  # Jika tidak ada command yang cocok

        return filters.create(func)

    async def start(self):
        """Menjalankan userbot dengan inisialisasi yang benar."""
        await super().start()
        
        try:
            await self.call_py.start()
        except Exception as e:
            print(f"[ERROR] Gagal memulai PyTgCalls: {e}")

        # Mengambil prefix yang tersimpan di database, default ke "."
        handler = await get_pref(self.me.id)
        self._prefix[self.me.id] = handler if handler else ["."]

        # Menambahkan instance ke daftar userbot
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"

        print(f"[✅ INFO] - ({self.me.id}) - BERHASIL DIMULAI")


# Inisialisasi bot utama
try:
    bot = Bot(
        name="bot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
    )
    print("[✅ INFO] Bot berhasil diinisialisasi.")
except Exception as e:
    print(f"[❌ ERROR] Gagal menginisialisasi bot: {e}")

# Inisialisasi userbot utama
try:
    ubot = Ubot(name="ubot")
    print("[✅ INFO] Userbot berhasil diinisialisasi.")
except Exception as e:
    print(f"[❌ ERROR] Gagal menginisialisasi userbot: {e}")


from DanteUserbot.core.database import *
from DanteUserbot.core.function import *
from DanteUserbot.core.helpers import *
