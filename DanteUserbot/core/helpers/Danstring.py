from DanteUserbot import *

class STR:
    async def PONG(client):
        str_pong = await get_vars(client.me.id, "STRING_PONG")
        string_pong = str_pong if str_pong else "⍜ ᴘᴏɴɢ"
        result = f"{string_pong}"
        return result

    async def OWNER(client):
        str_pong = await get_vars(client.me.id, "STRING_OWNER")
        string_pong = str_pong if str_pong else "⍜ ᴏᴡɴᴇʀ"
        result = f"{string_pong}"
        return result

    async def UBOT(client):
        str_pong = await get_vars(client.me.id, "STRING_UBOT")
        string_pong = str_pong if str_pong else "⍜ ᴜʙᴏᴛ"
        result = f"{string_pong}"
        return result

    async def DEVS(client):
        str_pong = await get_vars(client.me.id, "STRING_DEVS")
        string_pong = str_pong if str_pong else bot.me.mention
        result = f"{string_pong}"
        return result

    async def CUSTOM(client, var_name, default_value):
        str_custom = await get_vars(client.me.id, var_name)
        string_custom = str_custom if str_custom else default_value
        result = f"{string_custom}"
        return result
