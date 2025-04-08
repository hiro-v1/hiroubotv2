from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup
import re
from DanteUserbot import *


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    return re.findall(link_pattern, text)


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches

def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    for button_text, button_data in button_matches:
        data = (
            button_data.split(";same")[0]
            if detect_url_links(button_data.split(";same")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split(';same')[0]}"
        )
        cb_data = data if user_id else button_data.split(";same")[0]
        if button_data.startswith("http"):
            keyboard.append([InlineKeyboardButton(button_text, url=cb_data)])
        else:
            keyboard.append([InlineKeyboardButton(button_text, callback_data=cb_data)])

    if user_id and is_back:
        keyboard.append(
            [InlineKeyboardButton("Kembali", f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}")]
        )

    return InlineKeyboardMarkup(keyboard), text_matches

class Button:
    def alive(get_id):
        return [
            [
                InlineKeyboardButton("Tutup", callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}"),
                InlineKeyboardButton("Stats", callback_data="sys_stats"),
            ]
        ]

    def button_add_expired(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = [
            InlineKeyboardButton(f"{X} bulan", callback_data=f"success {user_id} {X}")
            for X in range(1, 13)
        ]
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"))
        buttons.row(InlineKeyboardButton("❌ Tolak Pembayaran", callback_data=f"failed {user_id}"))
        return buttons

    def expired_button_bot():
        return [
            [InlineKeyboardButton(text=f"{bot.me.first_name}", url=f"https://t.me/{bot.me.username}")]
        ]

    def start(message):
        """Tombol untuk menu utama."""
        print(f"[LOG] Membuat tombol untuk menu utama.")
        buttons = [
            [InlineKeyboardButton("🎁 Coba Gratis", callback_data="coba_gratis")],
            [InlineKeyboardButton("🆔 Cek ID", callback_data="cek_id")],
            [InlineKeyboardButton("🤖 Buat Userbot", callback_data="buat_ubot")],
            [InlineKeyboardButton("📚 Modul", callback_data="lihat_moduls")],
            [InlineKeyboardButton("☎️ Bantuan", callback_data="hubungi_owner")],
        ]
        return buttons

    def coba_gratis():
        """Tombol untuk fitur Coba Gratis."""
        print("[LOG] Membuat tombol 'Coba Gratis'")
        buttons = [
            [
                InlineKeyboardButton("🎁 Coba Gratis", callback_data="coba_gratis"),
                InlineKeyboardButton("🤖 Buat UBot", callback_data="buat_ubot"),
            ],
            [
                InlineKeyboardButton("📚 Moduls", callback_data="lihat_moduls"),
                InlineKeyboardButton("☎️ Bantuan", callback_data="hubungi_owner"),
            ],
            [
                InlineKeyboardButton("🆔 Cek ID", callback_data="cek_id"),
            ],
        ]
        return buttons

    def plus_minus(query, user_id):
        return [
            [
                InlineKeyboardButton("-1", callback_data=f"kurang {query}"),
                InlineKeyboardButton("+1", callback_data=f"tambah {query}"),
            ],
            [
                InlineKeyboardButton("Konfirmasi", callback_data="confirm"),
                InlineKeyboardButton("Kembali", callback_data="bahan"),
            ],
        ]

    def ambil_akun(user_id, count):
        return [
            [InlineKeyboardButton("📁 Hapus dari Database 📁", callback_data=f"del_ubot {int(user_id)}")],
            [InlineKeyboardButton("📲 Cek Nomor 📲", callback_data=f"get_phone {int(count)}")],
            [InlineKeyboardButton("⏳ Cek Kadaluarsa ⏳", callback_data=f"cek_masa_aktif {int(user_id)}")],
            [InlineKeyboardButton("🔑 Cek OTP 🔑", callback_data=f"get_otp {int(count)}")],
            [InlineKeyboardButton("🔐 Cek Verifikasi 2L 🔐", callback_data=f"get_faktor {int(count)}")],
            [InlineKeyboardButton("☠ Delete Account ☠", callback_data=f"ub_deak {int(count)}")],
            [InlineKeyboardButton("⬅️", callback_data=f"prev_ub {int(count)}"), InlineKeyboardButton("➡️", callback_data=f"next_ub {int(count)}")],
        ]

    def deak(user_id, count):
        return [
            [
                InlineKeyboardButton("Kembali", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("Setujui ✅", callback_data=f"deak_akun {int(count)}"),
            ],
        ]

def absen_hadir(get_id):
    return [[InlineKeyboardButton("Hadir", callback_data="hadir")]]

class INLINE:
    def QUERY(func):
        async def wrapper(client, inline_query):
            users = ubot._get_my_id
            if inline_query.from_user.id not in users:
                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=1,
                    results=[
                        InlineQueryResultArticle(
                            title=f"Anda belum order @{bot.me.username}",
                            input_message_content=InputTextMessageContent(
                                f"Silahkan order di @{bot.me.username} dulu biar bisa menggunakan inline ini"
                            ),
                        )
                    ],
                )
            else:
                await func(client, inline_query)
        return wrapper

    def DATA(func):
        async def wrapper(client, callback_query):
            users = ubot._get_my_id
            if callback_query.from_user.id not in users:
                await callback_query.answer(
                    f"Gak usah klik-klik mending langsung order di @{bot.me.username}",
                    True,
                )
            else:
                try:
                    await func(client, callback_query)
                except MessageNotModified:
                    await callback_query.answer("❌ ERROR")
        return wrapper

async def gcast_create_button(m):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = m.text.split("~>", 1)
    for X in split_text[1].split():
        button_data = X.split(":", 1)
        button_label = button_data[0].replace("_", " ")
        button_url = button_data[1]
        keyboard.append(InlineKeyboardButton(button_label, url=button_url))
    buttons.add(*keyboard)
    text_button = split_text[0].split(None, 1)[1]
    return buttons, text_button

async def notes_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = text.split("~>", 1)
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        button_url = split_X[1]
        keyboard.append(InlineKeyboardButton(button_text, url=button_url))
    buttons.add(*keyboard)
    text_button = split_text[0]
    return buttons, text_button

async def pmpermit_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = text.split("~>", 1)
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        button_url = split_X[1]
        keyboard.append(InlineKeyboardButton(button_text, url=button_url))
    buttons.add(*keyboard)
    text_button = split_text[0]
    return buttons, text_button
