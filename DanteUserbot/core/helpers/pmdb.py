import codecs
import pickle
import asyncio
from typing import Dict, List, Union
from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from DanteUserbot.config import MONGO_URL

mongo = MongoClient(MONGO_URL)
db = mongo
vardb = db["DanteUserbot"]["variable"]
permitdb = db["DanteUserbot"]["pmguard"]

async def add_approved_user(user_id):
    try:
        good_usr = int(user_id)
        does_they_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
        if does_they_exists:
            await permitdb.update_one(
                {"user_id": "APPROVED_USERS"}, {"$push": {"good_id": good_usr}}
            )
        else:
            await permitdb.insert_one({"user_id": "APPROVED_USERS", "good_id": [good_usr]})
    except Exception as e:
        print(f"Error adding approved user: {e}")

async def rm_approved_user(user_id):
    try:
        bad_usr = int(user_id)
        does_good_ones_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
        if does_good_ones_exists:
            await permitdb.update_one(
                {"user_id": "APPROVED_USERS"}, {"$pull": {"good_id": bad_usr}}
            )
        else:
            return None
    except Exception as e:
        print(f"Error removing approved user: {e}")

async def check_user_approved(user_id):
    try:
        random_usr = int(user_id)
        does_good_users_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
        if does_good_users_exists:
            good_users_list = does_good_users_exists.get("good_id", [])
            return random_usr in good_users_list
        return False
    except Exception as e:
        print(f"Error checking approved user: {e}")
        return False

async def set_var(user_id, var, value):
    try:
        vari = await vardb.find_one({"user_id": user_id, "var": var})
        if vari:
            await vardb.update_one(
                {"user_id": user_id, "var": var}, {"$set": {"vardb": value}}
            )
        else:
            await vardb.insert_one({"user_id": user_id, "var": var, "vardb": value})
    except Exception as e:
        print(f"Error setting var: {e}")

async def get_var(user_id, var):
    try:
        cosvar = await vardb.find_one({"user_id": user_id, "var": var})
        if not cosvar:
            return None
        else:
            return cosvar["vardb"]
    except Exception as e:
        print(f"Error getting var: {e}")
        return None

async def del_var(user_id, var):
    try:
        cosvar = await vardb.find_one({"user_id": user_id, "var": var})
        if cosvar:
            await vardb.delete_one({"user_id": user_id, "var": var})
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting var: {e}")
        return False
