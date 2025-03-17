import requests
from pyrogram.types import InputMediaPhoto, Message
import io
from pyrogram import Client, filters
from pyrogram.types import Message

from HiroUserbot import *

__MODULE__ = "ᴛᴏᴏʟs"
__HELP__ = f"""
**--chat GPT--**
<blockquote><b>
  <b>• perintah:</b> <code>{PREFIX[0]}ask</code>
  <b>• penjelasan:</b> buat pertanyaan contoh .ask dimana letak Antartika

tambahan:
  <b>• perintah:</b> <code>{PREFIX[0]}cp</code>
  <b>• penjelasan:</b> dapatkan poto profil couple pasangan.
  
</b></blockquote>"""

def get_text(message: Message) -> new_func(): # type: ignore
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

def new_func():
    return [None, str]

async def tanya(client, text):
    url = "https://itzpire.com/ai/botika"
    params = {
        "q": f"{text}",
        "user": f"{client, text.me.first_name}",
        "model": "sindy"
    }
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        msg = data["result"]
        return f"<blockquote>{msg}</blockquote>"
    else:
        return "Server error, gatau ah"

@HIRO.UBOT("ask")
async def gtp(client, message: Message):
    text = get_text(message)
    if not text:
        return await message.reply("perintah anda salah, gunakan .ask pertanyaan")
    pros = await message.reply("menjawab..")
    hasil = await tanya(client, text)
    return await pros.edit(hasil)
  
async def ambil_ppcp(message: Message):
    url = "https://itzpire.com/random/couple-pp"
    headers = {'accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Menangani kesalahan HTTP
        data = response.json()

        if data.get('status'):
            male_url = data.get('male')
            female_url = data.get('female')
            
            def download_image(url):
                img_response = requests.get(url)
                img_response.raise_for_status()  # Menangani kesalahan HTTP
                return io.BytesIO(img_response.content)

            male_image = download_image(male_url)
            female_image = download_image(female_url)
            
            media = [
                InputMediaPhoto(male_image, caption="Foto Profil Laki-laki\nDone ✔️"),
                InputMediaPhoto(female_image, caption="Foto Profil Perempuan\nDone ✔️")
            ]
            
            await message.reply_media_group(media)
        else:
            await message.reply("Gambar tidak ditemukan.")
    
    except requests.exceptions.RequestException as e:
        await message.reply(f"Terjadi kesalahan saat mengambil gambar: {str(e)}")
    except Exception as e:
        await message.reply(f"Kesalahan: {str(e)}")

@HIRO.UBOT("cp")
async def handle_ppcp(client: Client, message: Message):
    await ambil_ppcp(message)

async def pinterest(message: Message):
    url = "https://itzpire.com/search/pinterest"
    headers = {'accept': 'application/json'}
    
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get('status'):
        if 'url' in data and 'data' in data['url']:
            gambar_url = data['url']['data']
            deskripsi = data['url']['desc']
            return gambar_url, deskripsi
    return None, None


@HIRO.UBOT("pinter")
async def pinter(client, message: Message):
  text = message.text.split(" ")
  
  if len(text) < 3:
    
    return await message.reply(".pinter cari gambar di pinterest")
    
    message = text[1]
    
    gambar_url, deskripsi = await pinterest(message)
    
    if gambar_url:
        await message.reply_photo(photo=gambar_url, caption=f"<blockquote> link = <code>{deskripsi}</code></blockquote>")
    else:
        await message.reply("Gambar tidak tersedia atau tidak ada hasil.")
