from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
# Removed import of DanteUserbot.core.function to avoid circular import
from DanteUserbot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.tgcals_userbot
db = mongodb.premium
filtersdb = db.filters

# Import specific functions only when needed to avoid circular imports
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
from DanteUserbot.core.database.trial import is_trial_used, mark_trial_used
