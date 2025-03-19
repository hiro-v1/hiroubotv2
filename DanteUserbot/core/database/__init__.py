from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from DanteUserbot.__init__ import CustomMongoStorage  # Use CustomMongoStorage
from DanteUserbot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.tgcals_userbot
db = mongodb.premium
filtersdb = db.filters

from DanteUserbot.core.database.expired import *
from DanteUserbot.core.database.notes import *
from DanteUserbot.core.database.premium import *
from DanteUserbot.core.database.reseller import *
from DanteUserbot.core.database.saved import *
from DanteUserbot.core.database.DanteUserbot import *
from DanteUserbot.core.database.pref import *
from DanteUserbot.core.database.otp import *
from DanteUserbot.core.database.gbans import *
from DanteUserbot.core.database.setvar import *
from DanteUserbot.core.database.logger import *
from DanteUserbot.core.database.bcast import *
from DanteUserbot.core.database.permit import *
from DanteUserbot.core.database.filters import *
from DanteUserbot.core.database.expired import get_chat, get_expired_date, remove_chat
