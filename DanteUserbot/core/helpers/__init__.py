from DanteUserbot.core.helpers.client import *
from DanteUserbot.core.helpers.font_tool import *
from DanteUserbot.core.helpers.get_file_id import *
from DanteUserbot.core.helpers.inline import *
from DanteUserbot.core.helpers.kang_tool import *
from DanteUserbot.core.helpers.misc import *
from DanteUserbot.core.helpers.text import *
from DanteUserbot.core.helpers.unpack import *
from DanteUserbot.core.helpers.tools import *
from DanteUserbot.core.helpers.unpack import *
from DanteUserbot.core.helpers.uptime import *
from DanteUserbot.core.helpers.yt_dl import *
from DanteUserbot.core.helpers.msg_type import *
from DanteUserbot.core.helpers.queues import *
from DanteUserbot.core.helpers.handlers import *
from DanteUserbot.core.helpers.pmdb import *
from DanteUserbot.core.helpers.Danstring import *
from DanteUserbot.core.helpers.emoji import *

import os

def loadModule():
    """
    Function to load modules dynamically.
    Returns a list of module names.
    """
    modules_dir = os.path.join(os.path.dirname(__file__), "../modules")
    if not os.path.exists(modules_dir):
        print(f"⚠️ Directory '{modules_dir}' does not exist. Skipping module loading.")
        return []  # Return an empty list if the directory does not exist
    return [
        f[:-3]
        for f in os.listdir(modules_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]

__all__ = [
    "client",
    "font_tool",
    "get_file_id",
    "inline",
    "kang_tool",
    "misc",
    "text",
    "unpack",
    "tools",
    "uptime",
    "yt_dl",
    "msg_type",
    "queues",
    "handlers",
    "pmdb",
    "Danstring",
    "emoji",
    "loadModule",
]

