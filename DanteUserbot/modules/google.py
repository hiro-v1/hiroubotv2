import requests
from bs4 import BeautifulSoup
from googlesearch import search
from youtubesearchpython import VideosSearch

from DanteUserbot import *
from pyrogram.types import Message

__MODULE__ = "ɢᴏᴏɢʟᴇ ᴘᴇɴᴄᴀʀɪᴀɴ"

__HELP__ = f"""
**--ᴘᴇɴᴄᴀʀɪᴀɴ ᴍᴇʟᴀʟᴜɪ ɢᴏᴏɢʟᴇ, ɢᴀᴍʙᴀʀ, ᴅᴀɴ ʏᴏᴜᴛᴜʙᴇ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}google</code> [ᴋᴀᴛᴀ ᴋᴜɴᴄɪ]
  <b>• ᴇxᴘʟᴀɴᴀsɪ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴀʀɪ ɪɴꜰᴏʀᴍᴀsɪ ᴅɪ ɢᴏᴏɢʟᴇ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}crgambar</code> [ɢᴀᴍʙᴀʀ ʏᴀɴɢ ᴅɪɪɴɢɪɴᴋᴀɴ]
  <b>• ᴇxᴘʟᴀɴᴀsɪ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴀʀɪ ɢᴀᴍʙᴀʀ ᴅɪ ɢᴏᴏɢʟᴇ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ytsearch</code> [ᴊᴜᴅᴜʟ ᴠɪᴅᴇᴏ]
  <b>• ᴇxᴘʟᴀɴᴀsɪ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴀʀɪ ᴠɪᴅᴇᴏ ᴅɪ ʏᴏᴜᴛᴜʙᴇ.

  **ᴄᴏɴᴛᴏʜ ᴘᴇɴɢɢᴜɴᴀᴀɴ:**
  <b>🔍 ɢᴏᴏɢʟᴇ ᴘᴇɴᴄᴀʀɪᴀɴ</b>
  <code>{PREFIX[0]}google cara membuat kapal</code>

  <b>🖼 ᴍᴇɴᴄᴀʀɪ ɢᴀᴍʙᴀʀ</b>
  <code>{PREFIX[0]}crgambar mobil sport</code>

  <b>🎥 ᴍᴇɴᴄᴀʀɪ ᴠɪᴅᴇᴏ ʏᴏᴜᴛᴜʙᴇ</b>
  <code>{PREFIX[0]}ytsearch tutorial python</code>

</b></blockquote>
"""

async def google_search(query, num_results=5):
    """Melakukan pencarian teks di Google dan mengembalikan hasilnya."""
    results = []
    try:
        for j in search(query, tld="co.in", num=num_results, stop=num_results, pause=1):
            url = str(j)
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            site_title = soup.title.string if soup.title else "Tanpa Judul"

            meta_description = ""
            for meta in soup.find_all("meta"):
                if "name" in meta.attrs and meta.attrs["name"].lower() == "description":
                    meta_description = meta.attrs["content"]
                    break

            results.append(f"🔹 [{site_title}]({url})\n📝 {meta_description}\n")

    except Exception as e:
        results.append(f"⚠️ Error saat melakukan pencarian: {e}")

    return results


async def google_image_search(query, num_results=5):
    """Melakukan pencarian gambar di Google dan mengembalikan hasilnya."""
    url = f"https://www.google.com/search?hl=en&q={query.replace(' ', '+')}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")

        image_links = [img["src"] for img in images if "src" in img.attrs][1:num_results+1]
        return image_links

    except Exception as e:
        return [f"⚠️ Error saat mencari gambar: {e}"]


async def youtube_search(query, num_results=5):
    """Melakukan pencarian video di YouTube."""
    try:
        search_results = VideosSearch(query, limit=num_results).result()["result"]
        videos = [
            f"🎬 [{video['title']}]({video['link']}) - {video['duration']}"
            for video in search_results
        ]
        return videos
    except Exception as e:
        return [f"⚠️ Error saat mencari video: {e}"]


@DANTE.UBOT("google")
async def _(client, message: Message):
    """Command untuk mencari teks di Google."""
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Harap masukkan kata kunci pencarian!")

    query = " ".join(message.command[1:])
    await message.reply_text(f"🔍 **Mencari di Google...**\n`{query}`")
    
    results = await google_search(query)
    if not results:
        return await message.reply_text("⚠️ Tidak ada hasil yang ditemukan.")

    response = "\n".join(results)
    await message.reply_text(response, disable_web_page_preview=True)


@DANTE.UBOT("crgambar")
async def _(client, message: Message):
    """Command untuk mencari gambar di Google."""
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Harap masukkan kata kunci pencarian!")

    query = " ".join(message.command[1:])
    await message.reply_text(f"🖼 **Mencari gambar...**\n`{query}`")
    
    image_links = await google_image_search(query)
    if not image_links:
        return await message.reply_text("⚠️ Tidak ada gambar yang ditemukan.")

    for img in image_links:
        await message.reply_photo(img)


@DANTE.UBOT("ytsearch")
async def _(client, message: Message):
    """Command untuk mencari video di YouTube."""
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Harap masukkan kata kunci pencarian!")

    query = " ".join(message.command[1:])
    await message.reply_text(f"🎥 **Mencari video YouTube...**\n`{query}`")
    
    videos = await youtube_search(query)
    if not videos:
        return await message.reply_text("⚠️ Tidak ada video yang ditemukan.")

    response = "\n".join(videos)
    await message.reply_text(response, disable_web_page_preview=True)
