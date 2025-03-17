from HiroUserbot import *
import asyncio
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

CONFIRM_PAYMENT = []

@HIRO.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        button = [
            [
                InlineKeyboardButton("kembali", callback_data="bayar_dulu"),
                InlineKeyboardButton("batalkan", callback_data=f"home {user_id}"),
            ]
        ]                
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran anda: {full_name}</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )

    except asyncio.TimeoutError as out:
        if get.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get.id)
            await bot.send_message(get.id, "<blockquote>Waktu untuk mengirim bukti pembayaran telah habis. Silakan kirimkan kembali bukti pembayaran.</blockquote>")
            return    
    # except asyncio.TimeoutError as out:
        # if get.id in CONFIRM_PAYMENT:
            # CONFIRM_PAYMENT.remove(get.id)
            # return await bot.send_message(get.id, "pembatalan otomatis")
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran anda: {full_name}</b></blockquote>",
            )
            buttons = [[InlineKeyboardButton("✅ konfirmasi", callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """<blockquote>
<b>Tidak dapat di proses</b>

<b>Harap kirimkan screenshot bukti pembayaran anda yang valid</b>

<b>Silahkan konfirmasi ulang pembayaran anda</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = Button.button_add_expired(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran anda: {full_name}</b></blockquote>",
            )
            buttons = [
                [InlineKeyboardButton("admin", url=f"https://t.me/ProblematicCode")]
            ]
            return await bot.send_message(
                user_id,
                f"""<blockquote>
<b>Baik {full_name} Silahkan ditunggu dan jangan spam ya</b>
<b>pembayaran anda akan di konfirmasi setelah 1-12 jam kerja</b>
<b>jika pembayaran anda belum di konfirmasi silahkan hubungi admin</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )




@HIRO.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 20
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except:
        pass


@HIRO.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("⚒️ Buat NeverTech UBot", callback_data="memek")],
        ]
        await bot.send_message(
            get_user.id,
            f"""<blockquote>
<b>Pembayaran anda berhasil di konfirmasi </b>

<b>Sekarang anda bisa membuat HIROUserbot </b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(
                    "👤 dapatkan profil 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        await add_prem(get_user.id)
        now = datetime.now(timezone("asia/Jakarta"))
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
                    "💳 lakukan pembayaran 💳", callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            """<blockquote>
<b>Pembayaran anda tidak bisa di konfirmasi </b>

<b>Silahkan lakukan pembayaran dengan benar </b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(
                    "👤 dapatkan profil 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} Tidak ditambahkan ke anggota premium </b>
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
        else:
            buttons_home = Button.start(callback_query)
            return await callback_query.edit_message_text(
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
