import uvloop

uvloop.install()

import logging
import os
import re

from pyrogram import Client, filters
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.enums import ParseMode 
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from pytgcalls import GroupCallFactory
from pytgcalls.group_call_type import GroupCallType
from pytgcalls.mtproto_client_type import MTProtoClientType
from DanteUserbot.config import *
try:
    from aiohttp import ClientSession
except ImportError:
    print("aiohttp module is not installed. Please install it using 'pip install aiohttp'")

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
        super().__init__(**kwargs, device_model="hiro UBot")

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

    async def start(self):
        await super().start()


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
        self.call_py = self.group_call_factory.get(GroupCallType.RAW)  # Initialize call_py here
        self.device_model = "Dante UBot"
        
    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def pytgcalls_decorator(self):
        def decorator(func):
            for ub in self._ubot:
                if func.__name__ == "kicked_handler":
                    ub.call_py.on_update(
                        GroupCallParticipant(
                            GroupCallParticipant.Status.KICKED | GroupCallParticipant.Status.LEFT_GROUP,
                        )
                    )(func)
                elif func.__name__ == "stream_end_handler":
                    ub.call_py.on_update(GroupCallParticipant.stream_end)(func)
                elif func.__name__ == "participant_handler":
                    ub.call_py.on_update(
                        GroupCallParticipant(
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
        self._prefix[user_id] = prefix
    
    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    def cmd_prefix(self, cmd):
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

                    without_prefix = text[len(prefix) :]

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

                        return True

                return False

        return filters.create(func)

    async def start(self):
        await super().start()
        await self.call_py.start()  # Ensure call_py is started here
        handler = await get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"
        print(f"[𝐈𝐍𝐅𝐎] - ({self.me.id}) - 𝐒𝐓𝐀𝐑𝐓𝐄𝐃")

# Define a base class for CustomMongoStorage
class BaseStorage:
    async def open(self):
        pass

    async def close(self):
        pass

    async def save(self, key, value):
        raise NotImplementedError

    async def load(self, key):
        raise NotImplementedError

    async def delete(self, key):
        raise NotImplementedError

    async def clear(self):
        raise NotImplementedError

from motor.motor_asyncio import AsyncIOMotorClient

class CustomMongoStorage(BaseStorage):
    def __init__(self, uri, database, collection):
        self.client = AsyncIOMotorClient(uri)
        self.collection = self.client[database][collection]

    async def save(self, key, value):
        await self.collection.update_one(
            {"_id": key}, {"$set": {"value": value}}, upsert=True
        )

    async def load(self, key):
        document = await self.collection.find_one({"_id": key})
        return document["value"] if document else None

    async def delete(self, key):
        await self.collection.delete_one({"_id": key})

    async def clear(self):
        await self.collection.delete_many({})

# Remove the storage argument from Bot and Ubot initialization
bot = Client(
    "DanteUserbot",
    api_id=API_ID,  # Replace with your API ID
    api_hash=API_HASH,  # Replace with your API Hash
    bot_token=BOT_TOKEN  # Replace with your Bot Token
    # Removed storage argument
)

ubot = Ubot(
    name="ubot",
)

from DanteUserbot.core.database import *
from DanteUserbot.core.function import *
from DanteUserbot.core.helpers import *
