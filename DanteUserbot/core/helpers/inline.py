from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup
import re
from DanteUserbot import *


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches

def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split(";same")[0]
            if detect_url_links(button_data.split(";same")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split(';same')[0]}"
        )
        cb_data = data if user_id else button_data.split(";same")[0]
        if ";same" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    )
            else:
                if detect_url_links(cb_data):
                    button_row = [InlineKeyboardButton(button_text, url=cb_data)]
                else:
                    button_row = [
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    ]
                keyboard.append(button_row)
        else:
            if button_data.startswith("http"):
                button_row = [InlineKeyboardButton(button_text, url=cb_data)]
            else:
                button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "Kembali",
                    f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}",
                )
            ]
        )

    return markup, text_matches

class Button:
    def alive(get_id):
        button = [
            [
                InlineKeyboardButton(
                    text="tutup",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}"
                ),
                InlineKeyboardButton(
                    text="stats",
                    callback_data="sys_stats"
                ),
            ]
        ]
        return button

    def button_add_expired(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in range(1, 13):
            keyboard.append(
                InlineKeyboardButton(
                    f"{X} bulan",
                    callback_data=f"success {user_id} {X}",
                )
            )
        buttons.add(*keyboard)
        buttons.row(
            InlineKeyboardButton(
                "👤 profil", callback_data=f"profil {user_id}"
            )
        )
        buttons.row(
            InlineKeyboardButton(
                "❌ tolak pembayaran", callback_data=f"failed {user_id}"
            )
        )
        return buttons

    def expired_button_bot():
        button = [
            [
                InlineKeyboardButton(
                    text=f"{bot.me.first_name}",
                    url=f"https://t.me/{bot.me.username}",
                )
            ]
        ]
        return button

    def coba_gratis():
        """Tombol untuk fitur Coba Gratis."""
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

    def start(message):
        """Tombol untuk menu utama."""
        if message.from_user.id not in USER_ID:
            buttons = Button.coba_gratis()
        else:
            buttons = [
                [InlineKeyboardButton("Buat Userbot", callback_data="bahan")],
                [
                    InlineKeyboardButton("🛠 Update", callback_data="cb_gitpull"),
                    InlineKeyboardButton("Restart 🔄", callback_data="cb_restart"),
                ],
                [
                    InlineKeyboardButton("📋 Cek User", callback_data="cek_ubot"),
                    InlineKeyboardButton("Status Vps💾", callback_data="host"),
                ],
            ]
        return buttons

    def plus_minus(query, user_id):
        button = [
            [
                InlineKeyboardButton(
                    "-1",
                    callback_data=f"kurang {query}",
                ),
                InlineKeyboardButton(
                    "+1",
                    callback_data=f"tambah {query}",
                ),
            ],
            [
                InlineKeyboardButton("konfirmasi", callback_data="confirm"),
                InlineKeyboardButton("kembali", callback_data="bahan"),
            ]
        ]
        return button

    def ambil_akun(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 hapus dari database 📁",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "📲 cek nomor 📲",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ cek kadaluarsa ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔑 cek otp 🔑",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔐 cek verifikasi 2l 🔐",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "☠ delete account ☠", callback_data=f"ub_deak {int(count)}",
                )
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("➡️", callback_data=f"next_ub {int(count)}"),
            ],  
        ]
        return button

    def deak(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "kembali",
                    callback_data=f"prev_ub {int(count)}"
                ),
                InlineKeyboardButton(
                    "setuJui ✅", callback_data=f"deak_akun {int(count)}",
                ),
            ],
        ]
        return button

def absen_hadir(get_id):
    buttons = [
        [InlineKeyboardButton("Hadir", callback_data="hadir")],
    ]
    return buttons
                
       
class INLINE:
    def QUERY(func):
        async def wrapper(client, inline_query):
            users = ubot._get_my_id
            if inline_query.from_user.id not in users:
                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=1,
                    results=[
                        (
                            InlineQueryResultArticle(
                                title=f"anda belum order @{bot.me.username}",
                                input_message_content=InputTextMessageContent(
                                    f"silahkan order di @{bot.me.username} dulu biar bisa menggunakan inline ini"
                                ),
                            )
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
                    f"gak usah klik-klik mending Langsung order AE di @{bot.me.username}",
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
