import psutil # type: ignore
from time import time as waktunya, time
from os import getpid

from HiroUserbot import Bot
from HiroUserbot.core.helpers.client import DANTE
from HiroUserbot.core.helpers.inline import INLINE
from HiroUserbot.modules.youtube import time_formatter

start_time = waktunya()

async def get_time(seconds):
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ":"

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

# Ensure start_time is defined somewhere in the code
start_time = time()

@DANTE.CALLBACK("sys_stats")
@INLINE.DATA
async def _sys_callback(
    client,
    cq,
):
    text = sys_stats()
    await Bot.answer_callback_query(
        cq.id,
        text,
        show_alert=True,
    )

def sys_stats():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(getpid())
    stats = f"""
-----------------------
ᴜᴘᴛɪᴍᴇ: {time_formatter((time() - start_time) * 1000)}
ʙᴏᴛ: {round(process.memory_info()[0] / 1024 ** 2)} MB
ᴄᴘᴜ: {cpu}%
ʀᴀᴍ: {mem}%
ᴅɪsᴋ: {disk}%
-----------------------
"""
    return stats
