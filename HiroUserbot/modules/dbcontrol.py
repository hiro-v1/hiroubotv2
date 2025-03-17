from HiroUserbot import *
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from HiroUserbot.core.function.emoji import emoji
from HiroUserbot import *
from HiroUserbot.config import USER_ID
from .eval import *

async def prem_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴄᴇsɪɴɢ</b>...")
    if message.from_user.id not in await get_seles():
        return await Tm.edit(
            f"{ggl}<b>ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴄᴏᴍᴍᴀɴᴅ ɪɴɪ ᴀɴᴅᴀ ʜᴀʀᴜs ᴍᴇɴᴊᴀᴅɪ ʀᴇsᴇʟʟᴇʀ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>"
        )
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await Tm.edit(f"{ggl}<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʙᴜʟᴀɴ</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await Tm.edit(error)
    if not get_bulan:
        get_bulan = 1
    premium = await get_prem()
    if get_id in premium:
        return await Tm.edit(f"{sks}<b>ᴅɪᴀ sᴜᴅᴀʜ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>")
    added = await add_prem(get_id)
    if added:
        now = datetime.now(timezone("asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(get_id, expired)
        await Tm.edit(
            f"{sks}{get_id} ᴛᴇʟᴀʜ ᴅɪ ᴀᴋᴛɪғᴋᴀɴ sᴇʟᴀᴍᴀ {get_bulan} ʙᴜʟᴀɴ, sɪʟᴀʜᴋᴀɴ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅɪ @{bot.me.username}"
        )
        await bot.send_message(
            OWNER_ID,
            f"• {message.from_user.id} ─> {get_id} •",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 profil",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "profil 👤", callback_data=f"profil {get_id}"
                        ),
                    ],
                ]
            ),
        )
    else:
        await Tm.delete()
        await message.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")


async def unprem_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    if not user_id:
        return await Tm.edit(
            f"{ggl}<b>ʙᴀʟᴀs ᴘᴇsᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ʙᴇʀɪᴋᴀɴ ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(error)
    delpremium = await get_prem()
    if user.id not in delpremium:
        return await Tm.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    removed = await remove_prem(user.id)
    if removed:
        await Tm.edit(f"{sks}<b> {user.mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs</b>")
    else:
        await Tm.delete()
        await message.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")


async def get_prem_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    text = ""
    count = 0
    for user_id in await get_prem():
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    else:
        await message.reply(text)


async def add_blaclist(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.edit(f"{prs}<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    chat_id = message.chat.id
    blacklist = await get_chat(client.me.id)
    if chat_id in blacklist:
        return await Tm.edit(f"{sks}<b>ɢʀᴏᴜᴘ ɪɴɪ sᴜᴅᴀʜ ᴀᴅᴀ ᴅᴀʟᴀᴍ ʙʟᴀᴄᴋʟɪsᴛ</b>")
    add_blacklist = await add_chat(client.me.id, chat_id)
    if add_blacklist:
        await Tm.edit(f"{sks}<b>ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ</b>")
    else:
        await Tm.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")
        await asyncio.sleep(2)


async def del_blacklist(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.edit(f"<b>{prs}ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await Tm.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ</b>")
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await Tm.edit(f"{sks}<b>ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ</b>")
        else:
            await Tm.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")
    except Exception as error:
        await Tm.edit(error)
        await asyncio.sleep(2)


async def get_blacklist(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.edit(f"<b>{prs}ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    msg = f"<b>{prs}ᴛᴏᴛᴀʟ ʙʟᴀᴄᴋʟɪsᴛ {len(await get_chat(client.me.id))}</b>\n\n"
    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"{sks}<b>• {get.title} | <code>{get.id}</code></b>\n"
        except:
            msg += f"{sks}<b>• <code>{X}</code></b>\n"
    await message.edit(msg)


async def rem_all_blacklist(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    msg = await message.edit(f"{prs}<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs....</b>", quote=True)
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit(f"{ggl}<b>ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ ᴀɴᴅᴀ ᴋᴏsᴏɴɢ</b>")
    for X in get_bls:
        await remove_chat(client.me.id, X)
    await msg.edit(f"{sks}<b>sᴇᴍᴜᴀ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ ᴛᴇʟᴀʜ ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs</b>")


async def seles_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"{prs}<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    if not user_id:
        return await Tm.edit(
            f"{ggl}<b>ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ʙᴇʀɪᴋᴀɴ ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(error)
    reseller = await get_seles()
    if user.id in reseller:
        return await Tm.edit(f"{sks}<b>sᴜᴅᴀʜ ᴍᴇɴᴊᴀᴅɪ ʀᴇsᴇʟʟᴇʀ</b>.")
    added = await add_seles(user.id)
    if added:
        await add_prem(user.id)
        await Tm.edit(f"{sks}<b>{user.mention} ᴛᴇʟᴀʜ ᴍᴇɴᴊᴀᴅɪ ʀᴇsᴇʟʟᴇʀ</b>")
    else:
        await Tm.delete()
        await message.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")


async def unseles_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"{prs}<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    if not user_id:
        return await Tm.edit(
            f"{ggl}<b>ʙᴀʟᴀs ᴘᴇsᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ʙᴇʀɪᴋᴀɴ ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</n>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(error)
    delreseller = await get_seles()
    if user.id not in delreseller:
        return await Tm.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    removed = await remove_seles(user.id)
    if removed:
        await remove_prem(user.id)
        await Tm.edit(f"{sks}{user.mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs")
    else:
        await Tm.delete()
        await message.edit(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ</b>")


async def get_seles_user(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    text = ""
    count = 0
    for user_id in await get_seles():
        try:
            user = await bot.get_users(user_id)
            count += 1
            user = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{user}\n"
    if not text:
        await message.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    else:
        await message.edit(text)


# ========================== #
# 𝔻𝔸𝕋𝔸𝔹𝔸𝕊𝔼 𝔼𝕏ℙ𝕀ℝ𝔼𝔻 #
# ========================== #


async def expired_add(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    Tm = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    user_id, get_day = await extract_user_and_reason(message)
    if not user_id:
        return await Tm.edit(f"{ggl}<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʜᴀʀɪ</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"{sks}{get_id} <b>ᴛᴇʟᴀʜ ᴅɪᴀᴋᴛɪғᴋᴀɴ sᴇʟᴀᴍᴀ {get_day} ʜᴀʀɪ</b>.")


async def expired_cek(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴛᴇᴍᴜᴋᴀɴ</b>")
    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        await message.reply(f"{ggl}{user_id} <b>ʙᴇʟᴜᴍ ᴅɪᴀᴋᴛɪғᴋᴀɴ.</b>")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await message.reply(
            f"{sks}{user_id} ᴀᴋᴛɪғ ʜɪɴɢɢᴀ {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. sɪsᴀ ᴡᴀᴋᴛᴜ ᴀᴋᴛɪғ {remaining_days} ʜᴀʀɪ."
        )


async def un_expired(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"{prs}</b>ᴍᴇᴍᴘʀᴏsᴇs. . .</b>")
    if not user_id:
        return await Tm.edit(f"{ggl}<b>user ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    await rem_expired_date(user.id)
    return await Tm.edit(f"{sks}<b> {user.id} ᴇxᴘɪʀᴇᴅ ᴛᴇʟᴀʜ ᴅɪʜᴀᴘᴜs</b>")


async def bcast_cmd(_, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    
    if len(message.command) > 1:
        return await message.reply(
            f"<b>sɪʟᴀᴋᴀɴ sᴇʀᴛᴀᴋᴀɴ ᴘᴇsᴀɴ ᴀᴛᴀᴜ ʙᴀʟᴀs ᴘᴇsᴀɴ ʏᴀɴɢ ɪɴɢɪɴ ᴅɪsɪᴀʀᴋᴀɴ.</b>"
        )

    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for xx in babi:
        mmk.append(int(xx["user_id"]))
    if OWNER_ID in mmk:
        mmk.remove(OWNER_ID)
    for i in mmk:
        try:
            m = (
                await bot.forward_messages(i, y, x)
                if message.reply_to_message
                else await bot.send_message(i, y, x)
            )
            kntl += 1
        except:
            pass
    return await message.reply(
        f"** ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ `{kntl}` ᴘᴇɴɢɢᴜɴᴀ, ᴅᴀʀɪ `{jmbt}` ᴘᴇɴɢɢᴜɴᴀ.**",
    )

@HIRO.BOT("prem")
@HIRO.UBOT("prem")
@HIRO.SELES
async def _(client, message):
    await prem_user(client, message)

@HIRO.BOT("unprem")
@HIRO.UBOT("unprem")
@HIRO.SELES
async def _(client, message):
    await unprem_user(client, message)


@HIRO.BOT("getprem")
@HIRO.UBOT("getprem")
@HIRO.SELES
async def _(client, message):
    await get_prem_user(client, message)


@HIRO.BOT("seles")
@HIRO.UBOT("seles")
@HIRO.OWNER
async def _(client, message):
    await seles_user(client, message)


@HIRO.BOT("unseles")
@HIRO.UBOT("unseles")
@HIRO.OWNER
async def _(client, message):
    await unseles_user(client, message)


@HIRO.BOT("getseles")
@HIRO.UBOT("getseles")
@HIRO.OWNER
async def _(client, message):
    await get_seles_user(client, message)


@HIRO.BOT("time")
@HIRO.UBOT("time")
@HIRO.OWNER
async def _(client, message):
    await expired_add(client, message)


@HIRO.BOT("cek")
@HIRO.UBOT("cek")
@HIRO.OWNER
async def _(client, message):
    await expired_cek(client, message)


@HIRO.BOT("untime")
@HIRO.UBOT("untime")
@HIRO.OWNER
async def _(client, message):
    await un_expired(client, message)


@HIRO.CALLBACK("restart")
async def _(client, callback_query):
    await cb_restart(client, callback_query)


@HIRO.CALLBACK("gitpull")
@HIRO.OWNER
async def _(client, callback_query):
    await cb_gitpull(client, callback_query)


@HIRO.BOT("bcast")
@HIRO.OWNER
async def _(client, message):
    await bcast_cmd(client, message)

@HIRO.UBOT("addbl")
async def _(client, message):
    await add_blaclist(client, message)


@HIRO.UBOT("unbl")
async def _(client, message):
    await del_blacklist(client, message)


@HIRO.UBOT("rallbl")
async def _(client, message):
    await rem_all_blacklist(client, message)


@HIRO.UBOT("listbl")
async def _(client, message):
    await get_blacklist(client, message)