from DanteUserbot import *
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

CONFIRM_PAYMENT = []
USED_TRIAL = []

@DANTE.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)

    # Tambahkan ID ke CONFIRM_PAYMENT hanya jika belum ada di dalamnya
    if user_id not in CONFIRM_PAYMENT:
        CONFIRM_PAYMENT.append(user_id)

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

        if not pesan.photo:
            await pesan.request.edit(
                f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran anda: {full_name}</b></blockquote>",
            )
            buttons = [[InlineKeyboardButton("✅ konfirmasi", callback_data="confirm")]]
            await bot.send_message(
                user_id,
                """<blockquote>
<b>Tidak dapat di proses</b>

<b>Harap kirimkan screenshot bukti pembayaran anda yang valid</b>

<b>Silahkan konfirmasi ulang pembayaran anda</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return  # Exit point 1: Bukti pembayaran tidak valid

        # Jika bukti pembayaran valid, kirim ke admin
        buttons = Button.button_add_expired(user_id)
        await pesan.copy(
            OWNER_ID,
            reply_markup=buttons,
        )
        await pesan.request.edit(
            f"<blockquote><b>Silahkan kirimkan bukti screenshot pembayaran anda: {full_name}</b></blockquote>",
        )
        buttons = [
            [InlineKeyboardButton("admin", url="https://t.me/hiro_v1")]
        ]
        await bot.send_message(
            user_id,
            f"""<blockquote>
<b>Baik {full_name}, Silahkan ditunggu dan jangan spam ya</b>
<b>Pembayaran Anda akan dikonfirmasi dalam 1-12 jam kerja</b>
<b>Jika pembayaran belum dikonfirmasi, hubungi admin @hiro_v1</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except asyncio.TimeoutError:
        await bot.send_message(
            user_id, 
            "<blockquote>Waktu untuk mengirim bukti pembayaran telah habis. Silakan kirimkan kembali bukti pembayaran.</blockquote>"
        )
        return  # Exit point 2: Timeout terjadi

    finally:
        # Pastikan ID dihapus dari CONFIRM_PAYMENT di semua exit point
        if user_id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(user_id)


@DANTE.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])  # Ambil jumlah bulan
    HARGA = 20  # Harga per bulan
    QUERY = callback_query.data.split()[0]  # Aksi (kurang/tambah)

    TOTAL_HARGA = HARGA * BULAN  # Inisialisasi TOTAL_HARGA sebelum try

    try:
        if QUERY == "kurang" and BULAN > 1:
            BULAN -= 1
        elif QUERY == "tambah" and BULAN < 12:
            BULAN += 1

        TOTAL_HARGA = HARGA * BULAN  # Hitung ulang setelah perubahan BULAN
        
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error: {e}")  # Menampilkan error di log


@DANTE.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("⚒️ Buat hirov1 UBot", callback_data="memek")],
        ]
        await bot.send_message(
            get_user.id,
            f"""<blockquote>
<b>Pembayaran anda berhasil di konfirmasi </b>

<b>Sekarang anda bisa membuat HiroUserbot </b></blockquote>
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
