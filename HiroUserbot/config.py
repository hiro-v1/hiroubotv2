import os

DEVS = [
    5634309575
]
API_ID = int(os.getenv("API_ID", "25802693"))

API_HASH = os.getenv("API_HASH", "803393e9f1b6ea523853ce2126208c17")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8106338321:AAENpKKRGz8zMVvyefdToza_o_yolT5EGOo")

OWNER_ID = int(os.getenv("OWNER_ID", "5634309575"))

USER_ID = list(map(int,os.getenv("USER_ID", "5634309575",).split(),))

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1002159401394"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002159401394").split()))

MAX_BOT = int(os.getenv("MAX_BOT", "200"))

COMMAND = os.getenv("COMMAND", ".")

OPENAI_KEY = os.getenv("OPENAI_KEY")

SUDO_USER = os.getenv("SUDO_USER", "5634309575")

PREFIX = COMMAND.split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://siro22:hiro4636@cluster0.7ufff.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)
