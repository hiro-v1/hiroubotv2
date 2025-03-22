from pyrogram import filters
from pyrogram.enums import ChatType
from DanteUserbot import *
import re
from pyrogram.types import InlineKeyboardButton, CallbackQuery, InlineQuery  # Add InlineQuery to the imports

MSG = "Message Placeholder"  # Tambahkan definisi MSG sesuai kebutuhan

def Button(text, callback_data=None, url=None):
    """Helper function to create an InlineKeyboardButton."""
    return InlineKeyboardButton(text=text, callback_data=callback_data, url=url)

class FILTERS:
    ME = filters.me
    GROUP = filters.group
    PRIVATE = filters.private
    INCOMING = filters.incoming
    SERVICE = filters.service
    BOT = filters.bot
    OWNER = filters.user(OWNER_ID)
    DEV = filters.user(DEVS) & ~filters.me    
    ME_GROUP = filters.me & filters.group
    ME_OWNER = filters.me & filters.user(OWNER_ID)
    ME_USER = filters.me & filters.user(USER_ID)
    PM = filters.me & filters.private

SUDO_USER = "5634309575"

async def if_sudo(_, client, message):
    """Memastikan Owner selalu dalam daftar Sudo dan mengecek izin."""
    await ensure_owner_sudo(client.me.id)  # Pastikan Owner selalu ada di daftar Sudo
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")  # Ambil daftar Sudo

    is_user = message.from_user if message.from_user else message.sender_chat
    is_self = bool(message.from_user and message.from_user.is_self or getattr(message, "outgoing", False))

    return is_user.id in sudo_users or is_self

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

class DANTE:
    @staticmethod
    def MECHA():
        def decorator(func):
            return ubot.on_message(filters.create(list_kata) & ~filters.private & ~filters.me, group=10)(func)
        return decorator

    def DEVS(command, filter=FILTERS.DEV):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )

            @ubot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def BOT(command, filter=None):
        """Dekorator untuk perintah bot."""
        if not isinstance(command, (str, list)):
            raise TypeError(f"Command harus string atau list of strings, bukan {type(command).__name__}")

        command_filter = filters.command(command, prefixes=["/"])

        if filter is not None:
            if not isinstance(filter, filters.Filter):
                raise TypeError(f"Filter harus berupa Pyrogram filters, bukan {type(filter).__name__}")
            command_filter &= filter

        def wrapper(func):
            @bot.on_message(command_filter)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

        
    def OWNER(func):
        async def function(client, message):
            kon = message.from_user.id
            if kon != OWNER_ID:
                return
            return await func(client, message)

        return function
        
    def SELES(func):
        async def function(client, message):
            kon = message.from_user.id
            if kon not in await get_seles():
                return
            return await func(client, message)

        return function

    @staticmethod
    def UBOT(command, filter=None):
        """Dekorator untuk perintah userbot."""
        if not isinstance(command, (str, list)):
            raise TypeError(f"Command harus string atau list of strings, bukan {type(command).__name__}")

        command_filter = filters.command(command, prefixes=["/"])

        if filter is None:
            filter = filters.create(if_sudo)  # Pastikan hanya sudo user yang bisa menjalankan

        if not isinstance(filter, filters.Filter):
            raise TypeError(f"Filter harus berupa Pyrogram filters, bukan {type(filter).__name__}")

        def decorator(func):
            @ubot.on_message(command_filter & filter)
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func
 
        return decorator

    @staticmethod
    def ME_USER(command, filter=FILTERS.ME_USER):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )

            @ubot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def ADMIN(func):
        """Dekorator untuk memastikan hanya Admin/Sudo yang bisa menjalankan command."""
        async def function(client, message):
            await ensure_owner_sudo(client.me.id)
            admin_id = await get_list_from_vars(client.me.id, "SUDO_USER", "ID_NYA")
            if message.from_user.id not in admin_id:
                return  
            logging.info(f"[ADMIN] Perintah dari admin {message.from_user.id}")
            return await func(client, message)

        return function

        
    @staticmethod
    def NO_CMD_UBOT(result, ubot):
        query_mapping = {
            "AFK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                ),
                "group": 1,
            },
            "PMPERMIT": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.service
                ),
                "group": 2,
            },
            "LOGS_GROUP": {
                "query": (
                    filters.group
                    & filters.incoming
                    & filters.mentioned
                    & ~filters.bot
                ),
                "group": 3,
            },
            "LOGS_PRIVATE": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                ),
                "group": 4,
            },
        }
        result_query = query_mapping.get(result)

        def decorator(func):
            if result_query:
                async def wrapped_func(client, message):
                    await func(client, message)

                ubot.on_message(result_query["query"], group=int(result_query["group"]))(wrapped_func)
                return wrapped_func
            else:
                return func

        return decorator        
 
    @staticmethod
    def PRIVATE(func):
        """Dekorator untuk memastikan fungsi hanya berjalan di chat pribadi."""
        async def function(client, message):
            if message.chat.type != ChatType.PRIVATE:
                return  
            logging.info(f"[PRIVATE] Pesan dari {message.from_user.id}")
            return await func(client, message)

        return function

    @staticmethod
    def AFK(afk_no):
        """Dekorator untuk menangani status AFK."""
        def wrapper(func):
            afk_check = (
                (filters.mentioned | filters.private)
                & ~filters.bot
                & ~filters.me
                & filters.incoming
                if afk_no
                else filters.me & ~filters.incoming
            )

            @ubot.on_message(afk_check, group=10)
            async def wrapped_func(client, message):
                logging.info(f"[AFK] {message.from_user.id} memanggil pengguna AFK.")
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def TOP_CMD(func):
        """Dekorator untuk mencatat penggunaan command dalam database."""
        async def function(client, message):
            cmd = message.command[0].lower()
            top = await get_vars(bot.me.id, cmd, "modules")
            get = int(top) + 1 if top else 1
            await set_vars(bot.me.id, cmd, get, "modules")
            logging.info(f"[TOP_CMD] Perintah '{cmd}' digunakan oleh {message.from_user.id}")
            return await func(client, message)

        return function
      
    @staticmethod
    def GROUP(func):
        """Dekorator untuk memastikan fungsi hanya berjalan di grup atau supergrup."""
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return  
            logging.info(f"[GROUP] Pesan dari {message.from_user.id} di grup {message.chat.id}")
            return await func(client, message)

        return function
   


    @staticmethod
    def INLINE(command):
        """Dekorator untuk menangani inline query dengan regex filtering."""
        if not isinstance(command, str):
            raise TypeError("Command dalam INLINE harus berupa string.")

        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, inline_query: InlineQuery):
                logging.info(f"[INLINE] Query diterima: {inline_query.query}")

                # Cek parameter tambahan dari InlineQuery
                user_id = inline_query.from_user.id
                query_text = inline_query.query
                chat_type = inline_query.chat_type if inline_query.chat_type else "Unknown"
                location = inline_query.location if inline_query.location else "None"

                logging.info(f"[INLINE] User: {user_id}, ChatType: {chat_type}, Location: {location}")

                # Jika filter regex digunakan, kita bisa mendapatkan matches
                matches = inline_query.matches if hasattr(inline_query, "matches") else []

                # Panggil fungsi yang didekorasi dengan informasi tambahan
                await func(client, inline_query, query_text, matches, chat_type, location)

            return wrapped_func

        return wrapper


    @staticmethod
    def CALLBACK(command):
        """Dekorator untuk menangani callback query dengan regex filtering."""
        if not isinstance(command, str):
            raise TypeError("Command dalam CALLBACK harus berupa string.")

        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, callback_query: CallbackQuery):
                logging.info(f"[CALLBACK] Query diterima: {callback_query.data}")

                # Cek parameter tambahan dari CallbackQuery
                user_id = callback_query.from_user.id
                query_data = callback_query.data
                chat_instance = callback_query.chat_instance if callback_query.chat_instance else "None"
                inline_msg_id = callback_query.inline_message_id if callback_query.inline_message_id else "None"
                game_name = callback_query.game_short_name if callback_query.game_short_name else "None"

                logging.info(
                    f"[CALLBACK] User: {user_id}, ChatInstance: {chat_instance}, "
                    f"InlineMsgID: {inline_msg_id}, Game: {game_name}"
                )

                # Jika filter regex digunakan, kita bisa mendapatkan matches
                matches = callback_query.matches if hasattr(callback_query, "matches") else []

                # Panggil fungsi yang didekorasi dengan informasi tambahan
                await func(client, callback_query, query_data, matches, chat_instance, inline_msg_id, game_name)

            return wrapped_func

        return wrapper

        return wrapper  # Correctly indented
    @staticmethod
    def SUDO(command):
        """Dekorator untuk menangani command yang hanya bisa digunakan oleh Sudo Users."""
        if not isinstance(command, (str, list)):
            raise TypeError(f"Command harus berupa string atau list, bukan {type(command).__name__}")

        message_filter = filters.command(command, prefixes=["/"])

        async def is_sudo(_, client, message):
            await ensure_owner_sudo(client.me.id)
            sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")
            return message.from_user.id in sudo_users

        def wrapper(func):
            @ubot.on_message(message_filter & filters.create(is_sudo))
            async def wrapped_func(client, message):
                logging.info(f"[SUDO] Perintah '{command}' diterima dari {message.from_user.id}")
                return await func(client, message)

            return wrapped_func

        return wrapper
