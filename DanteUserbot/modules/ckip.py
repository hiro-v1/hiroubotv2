import base64
import aiohttp
from pyrogram import filters
from DanteUserbot import *
from DanteUserbot.core.function import eor

# API Key yang dikodekan dengan Base64
API_IP_LOOKUP = base64.b64decode("M0QwN0UyRUFBRjU1OTQwQUY0NDczNEMzRjJBQzdDMUE=").decode("utf-8")

async def fetch_json(url):
    """Fungsi untuk mengambil data JSON dari API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None

@DANTE.UBOT("ip")
async def lacak_ip(client, message):
    """Lacak lokasi IP Address"""
    if not API_IP_LOOKUP:
        return await message.reply("⚠️ API Key tidak ditemukan.")

    ran = await eor(message, "<code>Processing...</code>")
    if len(message.command) < 2:
        return await ran.edit("⚠️ Gunakan format: <code>.ip 192.168.1.1</code>")

    ip_address = message.command[1]
    url = f"https://api.ip2location.io/?key={API_IP_LOOKUP}&ip={ip_address}"
    
    data = await fetch_json(url)
    if not data:
        return await ran.edit("❌ Tidak dapat mengambil data lokasi.")

    try:
        result = (
            f"📌 <b>IP Address:</b> {data['ip']}\n"
            f"🌍 <b>Negara:</b> {data['country_name']} ({data['country_code']})\n"
            f"🏙️ <b>Kota:</b> {data['city_name']}\n"
            f"🗺️ <b>Wilayah:</b> {data['region_name']}\n"
            f"🕒 <b>Zona Waktu:</b> {data['time_zone']}\n"
            f"🔌 <b>Provider:</b> {data['as']}\n"
        )
        await ran.edit(result)
    except KeyError:
        await ran.edit("⚠️ IP tidak valid atau tidak ditemukan.")

@DANTE.UBOT("ipd")
async def whois_domain(client, message):
    """Cek WHOIS Domain"""
    if not API_IP_LOOKUP:
        return await message.reply("⚠️ API Key tidak ditemukan.")

    ran = await eor(message, "<code>Processing...</code>")
    if len(message.command) < 2:
        return await ran.edit("⚠️ Gunakan format: <code>.ipd google.com</code>")

    domain = message.command[1]
    url = f"https://api.ip2whois.com/v2?key={API_IP_LOOKUP}&domain={domain}"
    
    data = await fetch_json(url)
    if not data:
        return await ran.edit("❌ Tidak dapat mengambil data domain.")

    try:
        result = (
            f"🌐 <b>Domain:</b> {data['domain']}\n"
            f"📅 <b>Tanggal Dibuat:</b> {data['create_date']}\n"
            f"📆 <b>Update Terakhir:</b> {data['update_date']}\n"
            f"⏳ <b>Kadaluarsa:</b> {data['expire_date']}\n"
            f"🏢 <b>Organisasi:</b> {data['organization']}\n"
            f"📍 <b>Alamat:</b> {data['street_address']}, {data['city']}, {data['region']}, {data['country']}\n"
            f"📧 <b>Email:</b> {data['email']}\n"
            f"📞 <b>Telepon:</b> {data['phone']}\n"
            f"🖥️ <b>Server WHOIS:</b> {data['whois_server']}\n"
        )
        await ran.edit(result)
    except KeyError:
        await ran.edit("⚠️ Domain tidak valid atau tidak ditemukan.")

__MODULE__ = "ipsearch"
__HELP__ = f"""
<b>🔍 Bantuan Untuk IP & Domain Lookup</b>

• <code>.ip</code> <b>[IP Address]</b>
   ➜ <i>Melacak lokasi sebuah IP address.</i>
   Contoh: <code>.ip 8.8.8.8</code>

• <code>.ipd</code> <b>[Nama Domain]</b>
   ➜ <i>Melihat informasi WHOIS sebuah domain.</i>
   Contoh: <code>.ipd google.com</code>

