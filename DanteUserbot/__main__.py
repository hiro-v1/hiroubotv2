import asyncio

from pyrogram import idle
import os
from DanteUserbot import *
from pyrogram import Client
from atexit import register
from DanteUserbot.core.helpers.tools import *

async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
    except asyncio.TimeoutError:
        await remove_ubot(user_id)
        await add_prem(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await remove_all_vars(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        await sending_user(user_id)
        print(f"[𝗜𝗡𝗙𝗢] - ({user_id}) 𝗧𝗜𝗗𝗔𝗞 𝗗𝗔𝗣𝗔𝗧 𝗠𝗘𝗥𝗘𝗦𝗣𝗢𝗡")
    except Exception:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await remove_all_vars(user_id)
        await rem_pref(user_id)
        await rem_expired_date(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")

async def main():
    await bash("rm -rf *session*")
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_DanteUserbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await asyncio.gather(loadPlugins(), expiredUserbots(), idle())

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
