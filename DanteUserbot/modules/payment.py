from DanteUserbot import *
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

CONFIRM_PAYMENT = []

@DANTE.CALLBACK("^confirm")
async def confirm_payment(client, callback_query):
    user_id = callback_query.from_user.id
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)

    if user_id not in CONFIRM_PAYMENT:
        CONFIRM_PAYMENT.append(user_id)

    try:
        button = [
            [
                InlineKeyboardButton("Kembali", callback_data="bayar_dulu"),
                InlineKeyboardButton("Batalkan", callback_data=f"home {user_id}"),
            ]
        ]
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran Anda: {full_name}</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if user_id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(user_id)
        return await bot.send_message(
            user_id,
            "<blockquote>Waktu untuk mengirim bukti pembayaran telah habis. Silakan kirimkan kembali bukti pembayaran.</blockquote>",
        )

    if user_id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(user_id)
            await pesan.request.edit(
                f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran Anda: {full_name}</b></blockquote>",
            )
            buttons = [[InlineKeyboardButton("✅ Konfirmasi", callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """<blockquote>
<b>Tidak dapat diproses</b>

<b>Harap kirimkan screenshot bukti pembayaran Anda yang valid</b>

<b>Silahkan konfirmasi ulang pembayaran Anda</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            buttons = Button.button_add_expired(user_id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(user_id)
            await pesan.request.edit(
                f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran Anda: {full_name}</b></blockquote>",
            )
            buttons = [
                [InlineKeyboardButton("Admin", url="https://t.me/hiro_v1")]
            ]
            return await bot.send_message(
                user_id,
                f"""<blockquote>
<b>Baik {full_name}, Silahkan ditunggu dan jangan spam ya</b>
<b>Pembayaran Anda akan dikonfirmasi dalam 1-12 jam kerja</b>
<b>Jika pembayaran belum dikonfirmasi, hubungi admin @hiro_v1</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )

@DANTE.CALLBACK("confirm_payment")
async def confirm_payment(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.button_add_expired(user_id)
    await callback_query.message.edit_text(
        "✅ Bukti pembayaran Anda telah diterima. Silakan tunggu konfirmasi dari owner.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    await bot.send_message(
        OWNER_ID,
        f"📸 Bukti pembayaran dari <a href='tg://user?id={user_id}'>{user_id}</a>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@DANTE.CALLBACK("^(kurang|tambah)")
async def adjust_payment(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 20
    QUERY = callback_query.data.split()[0]

    try:
        if QUERY == "kurang" and BULAN > 1:
            BULAN -= 1
        elif QUERY == "tambah" and BULAN < 12:
            BULAN += 1

        TOTAL_HARGA = HARGA * BULAN
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error: {e}")

@DANTE.CALLBACK("^(success|failed|home)")
async def handle_payment_status(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])

    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("⚒️ Buat HiroUserbot", callback_data="memek")],
        ]
        await bot.send_message(
            get_user.id,
            f"""<blockquote>
<b>Pembayaran Anda berhasil dikonfirmasi</b>

<b>Sekarang Anda bisa membuat HiroUserbot</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(
                    "👤 Dapatkan Profil 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        await add_prem(get_user.id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(query[2]))
        await set_expired_date(get_user.id, expired)
        return await callback_query.edit_message_text(
            f"""
<b>✅ {get_user.first_name} {get_user.last_name or ''} ditambahkan ke anggota premium</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_success),
        )

    if query[0] == "failed":
        buttons = [
            [
                InlineKeyboardButton(
                    "💳 Lakukan Pembayaran 💳", callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            """<blockquote>
<b>Pembayaran Anda tidak bisa dikonfirmasi</b>

<b>Silahkan lakukan pembayaran dengan benar</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(
                    "👤 Dapatkan Profil 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} Tidak ditambahkan ke anggota premium</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_failed),
        )

    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
        buttons_home = Button.start(callback_query)
        return await callback_query.edit_message_text(
            MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(buttons_home),
        )
