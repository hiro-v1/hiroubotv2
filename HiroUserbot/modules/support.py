from HiroUserbot import *

import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from HiroUserbot import *

SUPPORT = []


async def support_callback(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    await callback_query.message.delete()
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("kembali", callback_data=f"home {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>silahkan kirim pertanyaan anda: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError as out:
        if get.id in SUPPORT:
            SUPPORT.remove(get.id)
            return await bot.send_message(get.id, "Pembatalan otomatis")
    text = f"<b>Pertanyaan anda sudah terkirim : {full_name}</b>"
    buttons = [
        [
            InlineKeyboardButton("👤 proꜰil", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("jawab 💬", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    if get.id in SUPPORT:
        try:
            await pesan.copy(
                OWNER_ID,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await pesan.request.edit(
                f"<b>Silahkan kirim pertanyaan Anda : {full_name}</b>"
            )
            return await bot.send_message(user_id, text)
        except Exception:
            pass
            return await bot.send_message(user_id, f"pesan berhasil di kirim✅")


async def jawab_pesan_callback(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("batalkan", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>Silahkan kirim balasan Anda: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if get.id in SUPPORT:
            SUPPORT.remove(get.id)
            return await bot.send_message(get.id, "Pembatalan otomatis")
    text = f"<b>Pesan balasan anda telah terkirim : {full_name}</b>"
    if not user_ids == OWNER_ID:
        buttons = [[InlineKeyboardButton("💬 jawab pesan 💬", f"jawab_pesan {user_id}")]]
    else:
        buttons = [
            [
                InlineKeyboardButton("👤 proꜰil", callback_data=f"profil {user_id}"),
                InlineKeyboardButton("jawab 💬", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    if get.id in SUPPORT:
        try:
            await pesan.copy(
                user_ids,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await pesan.request.edit(
                f"<b>Silahkan kirim balasan anda: {full_name}</b>",
            )
            await bot.send_message(user_id, text)
        except Exception:
            pass
            return await bot.send_message(user_id, f"pesan berhasil di kirim✅")


async def profil_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await bot.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ id pengguna:</b> <code>{get.id}</code>\n"
            f"<b> ┣ nama depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ nama belakangnya:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ username:</b> @{username}\n"
        msg += f"<b> ┗ bot: {bot.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(why)


async def batal_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    if user_id in SUPPORT:
        try:
            SUPPORT.remove(user_id)
            await callback_query.message.delete()
            buttons = Button.start(callback_query)
            return await bot.send_message(
                user_id,
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as why:
            await callback_query.message.delete()
            await bot.send_message(user_id, f"<b>gagal di batalkan! {why}</b>")

@HIRO.CALLBACK("^support")
async def _(client, callback_query):
    await support_callback(client, callback_query)


@HIRO.CALLBACK("^jawab_pesan")
async def _(client, callback_query):
    await jawab_pesan_callback(client, callback_query)


@HIRO.CALLBACK("^profil")
async def _(client, callback_query):
    await profil_callback(client, callback_query)


@HIRO.CALLBACK("^batal")
async def _(client, callback_query):
    await batal_callback(client, callback_query)
