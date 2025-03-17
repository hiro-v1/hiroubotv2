import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from HiroUserbot import bot, ubot
from HiroUserbot.config import LOGS_MAKER_UBOT
from HiroUserbot.core.database import (get_chat, get_expired_date,
                                    rem_expired_date, remove_chat, remove_ubot,
                                    rm_all)
from HiroUserbot.core.helpers import MSG, Button


async def expiredUserbots():
    while True:
        for X in ubot._ubot:
            try:
                time = datetime.now(timezone("asia/Jakarta")).strftime("%d-%m-%Y")
                exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
                if time == exp:
                    await X.unblock_user(bot.me.username)
                    for chat in await get_chat(X.me.id):
                        await remove_chat(X.me.id, chat)
                    await rm_all(X.me.id)
                    await remove_ubot(X.me.id)
                    await rem_expired_date(X.me.id)
                    ubot._get_my_id.remove(X.me.id)
                    ubot._ubot.remove(X)
                    await X.log_out()
                    await bot.send_message(
                        LOGS_MAKER_UBOT,
                        MSG.EXPIRED_MSG_BOT(X),
                        reply_markup=InlineKeyboardMarkup(Button.expired_button_bot()),
                    )
                    await bot.send_message(
                        X.me.id, "<b>💬 masa aktif anda telah berakhir"
                    )
            except Exception as e:
                print(f"Error: - {X.me.id} - :{str(e)}")
        await asyncio.sleep(10)
