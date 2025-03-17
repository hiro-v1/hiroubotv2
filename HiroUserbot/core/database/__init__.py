from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from HiroUserbot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.tgcals_userbot
db = mongodb.premium
filtersdb = db.filters

from HiroUserbot.core.database.expired import *
from HiroUserbot.core.database.notes import *
from HiroUserbot.core.database.premium import *
from HiroUserbot.core.database.reseller import *
from HiroUserbot.core.database.saved import *
from HiroUserbot.core.database.HiroUserbot import *
from HiroUserbot.core.database.pref import *
from HiroUserbot.core.database.otp import *
from HiroUserbot.core.database.gbans import *
from HiroUserbot.core.database.setvar import *
from HiroUserbot.core.database.logger import *
from HiroUserbot.core.database.bcast import *
from HiroUserbot.core.database.permit import *
from HiroUserbot.core.database.filters import *
