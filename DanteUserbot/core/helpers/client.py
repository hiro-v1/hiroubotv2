from pyrogram import filters
from pyrogram.enums import ChatType
from DanteUserbot import *
import re

# 🔹 Filter khusus untuk bot dan pengguna tertentu
class FILTERS:
    ME = filters.me
    GROUP = filters.group
    PRIVATE = filters.private
    INCOMING = filters.incoming
    SERVICE = filters.service
    BOT = filters.bot
    OWNER = filters.user(OWNER_ID)  # Lebih aman dan sesuai standar
    DEV = filters.user(DEVS) & ~filters.me
    ME_GROUP = filters.me & filters.group
    ME_OWNER = filters.me & filters.user(OWNER_ID)
    ME_USER = filters.me & filters.user(USER_ID)
    PM = filters.me & filters.private

SUDO_USER = "5634309575"

# ✅ Cek apakah pengguna adalah SUDO
async def if_sudo(_, client, message):
    await ensure_owner_sudo(client.me.id)
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")

    is_user = message.from_user if message.from_user else message.sender_chat
    is_self = message.from_user and message.from_user.is_self or getattr(message, "outgoing", False)

    return is_user.id in sudo_users or is_self

# ✅ Cek apakah pesan mengandung kata dalam daftar tertentu
async def list_kata(_, client, message):
    is_on = await get_status(client.me.id)
    if not is_on:
        return False

    word_list = await get_vars(client.me.id, "WORD_LIST") or []
    if not message.text:
        return False

    message_text = message.text.lower()
    pattern = r'\b(?:' + '|'.join(re.escape(word.lower()) for word in word_list) + r')\b'
    return bool(re.search(pattern, message_text))

# ✅ Kelas utama untuk menangani berbagai decorator di DanteUserbot
class DANTE:

    @staticmethod
    def UBOT(command: str, filter=None):
        """Decorator untuk menangani command yang hanya bisa digunakan oleh Sudo."""
        if filter is None:
            filter = filters.create(if_sudo)  # Gunakan if_sudo untuk memfilter pengguna Sudo
        
        def decorator(func):
            @ubot.on_message(filters.command(command) & filter)
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as e:
                    print(f"⚠️ Error UBOT command {command}: {e}")
            return wrapped_func
        return decorator

    @staticmethod
    def INLINE(command: str):
        """Decorator untuk menangani inline query dengan regex filter."""
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, inline_query):
                await func(client, inline_query)
            return wrapped_func
        return wrapper

    @staticmethod
    def CALLBACK(command: str):
        """Decorator untuk menangani callback query dengan regex filter."""
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, callback_query):
                try:
                    await func(client, callback_query)
                except Exception as e:
                    print(f"⚠️ Error CALLBACK {command}: {e}")
            return wrapped_func
        return wrapper

    @staticmethod
    def SUDO(command: str):
        """Decorator untuk menangani command yang hanya bisa digunakan oleh Sudo Users."""
        async def is_sudo(_, client, message):
            await ensure_owner_sudo(client.me.id)
            sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")
            return message.from_user.id in sudo_users

        def wrapper(func):
            @ubot.on_message(filters.create(is_sudo) & filters.command(command))
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as e:
                    print(f"⚠️ Error SUDO command {command}: {e}")
            return wrapped_func
        return wrapper

    @staticmethod
    def ADMIN(func):
        """Decorator untuk memastikan hanya Admin/Sudo yang bisa menjalankan command."""
        async def function(client, message):
            await ensure_owner_sudo(client.me.id)
            admin_id = await get_list_from_vars(client.me.id, "SUDO_USER")

            if message.from_user.id not in admin_id:
                return  # Abaikan jika bukan admin
            return await func(client, message)

        return function

    @staticmethod
    def GROUP(func):
        """Decorator untuk memastikan command hanya bisa digunakan di grup."""
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return
            return await func(client, message)
        return function

    @staticmethod
    def PRIVATE(func):
        """Decorator untuk memastikan command hanya bisa digunakan di private chat."""
        async def function(client, message):
            if message.chat.type != ChatType.PRIVATE:
                return
            return await func(client, message)
        return function

    @staticmethod
    def AFK(afk_no: bool):
        """Decorator untuk menangani mode AFK."""
        def wrapper(func):
            afk_filter = (
                (filters.mentioned | filters.private) & ~filters.bot & ~filters.me & filters.incoming
                if afk_no else
                filters.me & ~filters.incoming
            )

            @ubot.on_message(afk_filter, group=10)
            async def wrapped_func(client, message):
                await func(client, message)
            return wrapped_func
        return wrapper

    @staticmethod
    def TOP_CMD(func):
        """Decorator untuk mencatat penggunaan command."""
        async def function(client, message):
            cmd = message.command[0].lower()
            top = await get_vars(bot.me.id, cmd, "modules")
            get = int(top) + 1 if top else 1
            await set_vars(bot.me.id, cmd, get, "modules")
            return await func(client, message)
        return function
