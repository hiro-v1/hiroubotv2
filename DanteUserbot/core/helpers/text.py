from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from DanteUserbot.config import LOGS_MAKER_UBOT, OWNER_ID
from DanteUserbot import bot, ubot
from DanteUserbot.core.database import get_expired_date

class MSG:
    def DEAK(X):
        return f"""<blockquote>
<b>❏ pemberitahuan</b>
<b>├ akun:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ id:</b> <code>{X.me.id}</code>
<b>╰ telah berhasil di hapus dari telegram</b></blockquote>
"""
            
    def EXPIRED_MSG_BOT(X):
        return f"""<blockquote>
<b>❏ pemberitahuan</b>
<b>├ akun:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ id:</b> <code>{X.me.id}</code>
<b>╰ masa aktif telah habis</b></blockquote>
"""

    
    def START(message):
        print(f"[LOG] Fungsi MSG.START dipanggil untuk {message.from_user.id}")
        return f"""<blockquote>
<b>Hallo <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>
🤖 saya adalah pembuat <b><u>userbot telegram</b></u> 

🚦 saya memiliki modul yang lengkap untuk membantu aktivitas anda di Telegram, jika kamu penasaran dengan modul saya, silahkan cek di modul

⚠️ jika kamu ingin menggunakan userbot ini <b><u>klik tombol buat userbot dibawah</b></u>
</blockquote>
"""

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""<blockquote>
sɪʟᴀᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ

ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: {harga}.000

💳 ᴍᴇᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:
 ├──• DANA
 ├─• <a href='https://t.me/hiro_v1'>Owner</a>


🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: Rp {total}.000
🗓️ ᴛᴏᴛᴀʟ ʙᴜʟᴀɴ: {bulan}

✅ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍᴋᴀɴ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ
</blockquote>"""

    async def USERBOT(count):
        expired_date = await get_expired_date(ubot._ubot[int(count)].me.id)
        return f"""<blockquote>
<b>❏ userbot ke</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ akun:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ├ id:</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b> ╰ expired</b> <code>{expired_date.strftime('%d-%m-%Y')}</code>
</blockquote>"""

    def POLICY():
        return """<blockquote>
Kebijakan Pengembalian:

Setelah melakukan pembayaran, jika anda belum menerima manfaat dari pembelian, 
anda berhak untuk mengajukan pengembalian dalam waktu 2 hari setelah pembelian. 
Namun, jika anda telah menggunakan atau menerima salah satu manfaat dari pembelian, 
termasuk akses ke fitur pembuatan userbot, maka anda tidak lagi memenuhi syarat untuk pengembalian dana.

Dukungan:

Untuk mendapatkan bantuan atau dukungan, 
anda dapat menghubungi admin di bawah ini atau mengirim pesan ke <a href='https://t.me/hiro_v1'>Owner</a> Harap diingat, jangan menghubungi Dukungan Telegram atau Dukungan Bot untuk masalah terkait pembayaran yang dilakukan di bot ini.

Tombol Lanjutkan:

Klik tombol "Lanjutkan" untuk mengkonfirmasi 
bahwa anda telah membaca dan menerima ketentuan ini dan 
melanjutkan proses pembelian. Jika tidak, klik tombol "Kembali".
</blockquote>"""

    def PLUGINS_ACTIVATED(bot, ubot, python_version, pyrogram_version, modules_count):
        return f"""<blockquote>
<b>🤖 {bot.me.mention} berhasil diaktifkan</b>

<b>📁 Modules: {modules_count}</b>
<b>📘 Python: {python_version}</b>
<b>📙 Pyrogram: {pyrogram_version}</b>

<b>👤 DanteUserbot: {len(ubot._ubot)}</b>
</blockquote>"""


async def sending_user(user_id):
    try:
        if bot and bot.me and bot.me.username:
            await bot.send_message(
                user_id,
                "⚠️ Silahkan buat ulang userbot kamu!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Buat Userbot",
                                callback_data="bahan",
                            )
                        ],
                    ]
                ),
                disable_web_page_preview=True,
            )
            await bot.send_message(
                LOGS_MAKER_UBOT,
                f"""
<blockquote>➡️ yang merasa memiliki id: {user_id}

✅ silahkan buat ulang userbot nya di: @{bot.me.username}</blockquote>
        """,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📁 cek masa aktif 📁",
                                callback_data=f"cek_masa_aktif {user_id}",
                            )
                        ],
                    ]
                ),
                disable_web_page_preview=True,
            )
        else:
            print("Bot belum diinisialisasi dengan benar atau atribut 'me' tidak tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        # Lakukan penanganan kesalahan sesuai kebutuhan anda
