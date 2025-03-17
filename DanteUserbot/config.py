import os

DEVS = [
    1282758415
]
API_ID = int(os.getenv("API_ID", "22588918"))

API_HASH = os.getenv("API_HASH", "03111b1410101a2125625a532fb954f6")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7419564990:AAGXrQmNxbJx-DqJykWmR3KZ86Kh4eeFLVw")

OWNER_ID = int(os.getenv("OWNER_ID", "1282758415"))

USER_ID = list(map(int,os.getenv("USER_ID", "1282758415",).split(),))

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1002159401394"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002159401394").split()))

MAX_BOT = int(os.getenv("MAX_BOT", "200"))

COMMAND = os.getenv("COMMAND", ".")

OPENAI_KEY = os.getenv("OPENAI_KEY")

SUDO_USER = os.getenv("SUDO_USER", "1282758415")

PREFIX = COMMAND.split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://yigobi4317:Hirogant1234$@cluster0.kvg0g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
