from pyrogram import filters
from pyrogram.enums import ChatType
from HiroUserbot import *
import re

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

SUDO_USER = "940232666"

async def if_sudo(_, client, message):
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER", "ID_NYA")
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

class HIRO:
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
        
    def BOT(command, filter=FILTERS.PRIVATE):
        def wrapper(func):
            @bot.on_message(filters.command(command) & filter)
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
        if filter is None:
            filter = filters.create(if_sudo)

        def decorator(func):
            @ubot.on_message(ubot.cmd_prefix(command) & filter)
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
        async def function(client, message):
            user = message.from_user
            admin_id = await get_list_from_vars(client.me.id, "SUDO_USER", "ID_NYA")
            if user.id not in admin_id:
                return
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
        async def function(client, message):
            if not message.chat.type == ChatType.PRIVATE:
                return 
            return await func(client, message)

        return function

    @staticmethod
    def AFK(afk_no):
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
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def TOP_CMD(func):
        async def function(client, message):
            cmd = message.command[0].lower()
            top = await get_vars(bot.me.id, cmd, "modules")
            get = int(top) + 1 if top else 1
            await set_vars(bot.me.id, cmd, get, "modules")
            return await func(client, message)

        return function
        
    @staticmethod
    def GROUP(func):
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return 
            return await func(client, message)

        return function     

    def INLINE(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
