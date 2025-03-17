import requests
from pyrogram.types import Message, InputMediaPhoto 
import io
from pyrogram import Client, filters

from DanteUserbot import *

__MODULE__ = "ᴛᴏᴏʟs"
__HELP__ = f"""
**--chat GPT--**
<blockquote><b>

  <b>• perintah:</b> <code>{PREFIX[0]}gbr</code>
  <b>• penjelasan:</b> buat cari gambar contoh .gbr kucing
  <b>• perintah:</b> <code>{PREFIX[0]}cp</code>
  <b>• penjelasan:</b> buat cari PPCP contoh .cp
  <b>• perintah:</b> <code>{PREFIX[0]}ask</code>
  <b>• penjelasan:</b> buat pertanyaan contoh .ask berapa panas bumi
  tambahan:
  <b>• interaksi sama alicia:</b> 
  <b> .ask si hiro ko cuek banget kenapa ya? apa dia ga sayang aku lagi
  <b> .ask alice kamu udah cuci piring?
  
</b></blockquote>"""

def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def tanya(client, text):
    url = "https://itzpire.com/ai/botika"
    params = {
        "q": f"{text}",
        "user": f"{client.me.first_name}",
        "model": "alicia"
    }
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        msg = data["result"]
        return f"<blockquote>{msg}</blockquote>"
    else:
        return "Server error, gatau ah"

@DANTE.UBOT("ask")
async def gpt(client, message: Message):
    text = get_text(message)
    if not text:
        return await message.reply("perintah anda salah, gunakan .ask pertanyaan")
    pros = await message.reply("gue jawab..")
    hasil = await tanya(client, text)
    return await pros.edit(hasil)

PEXELS_API_KEY = "bW3YvusBW8JPjUnwoF5K4RKWorvqkDCADXxl8Hz2mk9T6hpjdbi55hhv"

async def fetch_pexels_images(query="profile", per_page=2):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}"
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Menangani kesalahan HTTP
        data = response.json()

        if "photos" in data and len(data["photos"]) >= per_page:
            return [photo["src"]["original"] for photo in data["photos"][:per_page]]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

async def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

async def ambil_ppcp(message: Message):
    images = await fetch_pexels_images()

    if images:
        male_image = await download_image(images[0])
        female_image = await download_image(images[1])

        if male_image and female_image:
            media = [
                InputMediaPhoto(male_image, caption="Foto Profil Laki-laki\nDone ✔️"),
                InputMediaPhoto(female_image, caption="Foto Profil Perempuan\nDone ✔️")
            ]
            await message.reply_media_group(media)
        else:
            await message.reply("Gagal donlod coba yang laen.")
    else:
        await message.reply("gambar ga ada lu jelek kali.")

@Client.on_message(filters.command("cp"))
async def handle_ppcp(client: Client, message: Message):
    await ambil_ppcp(message)

@Client.on_message(filters.command("gbr"))
async def pinter(client, message: Message):
    text = message.text.split(" ", 1)

    if len(text) < 2:
        return await message.reply("Gunakan format: `gbr [kata_kunci]`\nContoh: `gbr anime`")

    query = text[1]  # Kata kunci pencarian
    images = await fetch_pexels_images(query=query, per_page=1)

    if images:
        await message.reply_photo(
            photo=images[0],
            caption=f"<b>🔍 Hasil pencarian untuk:</b> <code>{query}</code>\n"
                    f"<b>📸 Sumber:</b> <a href='https://www.pexels.com'>Pexels</a>",
            parse_mode="html",
        )
    else:
        await message.reply("Gambar ga ada, coba cari yang laen.")
