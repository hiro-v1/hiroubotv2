import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from DanteUserbot.config import OWNER_ID
import psutil
from DanteUserbot import *

@DANTE.UBOT("update")
async def ngentod(client, message):
    if message.from_user.id != OWNER_ID:
        return
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(out, quote=True)
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"```{out}```", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "DanteUserbot")