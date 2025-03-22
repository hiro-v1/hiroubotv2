from DanteUserbot import *

__MODULE__ = "ᴛʀᴀɴsʟᴀᴛᴇ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴛʀᴀɴsʟᴀᴛᴇ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}tr</code> [ʀᴇᴘʟʏ/ᴛᴇxᴛ]
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴇʀᴊᴇᴍᴀʜᴋᴀɴ ᴛᴇxᴛ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}bahasa</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʀᴜʙᴀʜ ʙᴀʜᴀsᴀ ᴛʀᴀɴsʟᴀᴛᴇ

  ɴᴏᴛᴇ : ᴀᴛᴜʀ ʙᴀʜᴀsᴀ ᴅᴀʜᴜʟᴜ ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ғɪᴛᴜʀ ɪɴɪ</b></blockquote>
"""

import os
from gc import get_objects

import gtts
from gpytranslate import Translator
from pykeyboard import InlineKeyboard

from DanteUserbot import *


async def tts_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    jdl = await EMO.JUDUL(client)
    try:
        TM = await message.reply(f"<b>{prs}ᴘʀᴏᴄᴄᴇsɪɴɢ...</b>")
        if message.reply_to_message:
            language = client._translate[client.me.id]["negara"]
            words_to_say = message.reply_to_message.text or message.reply_to_message.caption
        else:
            if len(message.command) < 2:
                return await TM.edit(f"{ggl}<code>{message.text}</code> <b>ʙᴇʀɪᴋᴀɴ ᴛᴇᴋs ᴀᴛᴀᴜ ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ!</b>")
            else:
                language = client._translate[client.me.id]["negara"]                
                words_to_say = message.text.split(None, 1)[1]
        speech = gtts.gTTS(words_to_say, lang=language)
        speech.save("text_to_speech.oog")
        rep = message.reply_to_message or message
    except TypeError:
        return await TM.edit(f"{ggl}<b>ᴍᴏʜᴏɴ sᴇᴛᴛɪɴɢ ʙᴀʜᴀsᴀ ᴅᴜʟᴜ !</b>")
    try:
        await client.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=rep.id,
        )
        await TM.delete()
    except Exception as error:
        await TM.edit(error)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass


async def tr_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    try:
        trans = Translator()
        TM = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴄᴇsɪɴɢ..</b>")
        if message.reply_to_message:
            dest = client._translate[client.me.id]["negara"]
            to_translate = message.reply_to_message.text or message.reply_to_message.caption
            source = await trans.detect(to_translate)
        else:
            if len(message.command) < 2:
                return await message.reply(f"<code>{message.text}</code> reply/text")
            else:
               dest = client._translate[client.me.id]["negara"]
               to_translate = message.text.split(None, 1)[1]
               source = await trans.detect(to_translate)
        translation = await trans(to_translate, sourcelang=source, targetlang=dest)
        reply = f"<code>{translation.text}</code>"
        rep = message.reply_to_message or message
        await TM.delete()
        await client.send_message(message.chat.id, reply, reply_to_message_id=rep.id)
    except TypeError:
        await message.reply_text(f"{ggl}<b>ᴍᴏʜᴏɴ sᴇᴛᴛɪɴɢ ʙᴀʜᴀsᴀ ᴅᴜʟᴜ ᴋᴇᴛɪᴋ</b> <code>.bahasa</code>")
    except Exception as r:
        await TM.delete()
        await message.reply_text(r)

async def set_lang_cmd(client, message):
    query = id(message)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"ubah_bahasa {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


async def ubah_bahasa_inline(client, inline_query):
    """Handle inline query for changing language."""
    buttons = InlineKeyboard(row_width=3)
    keyboard = [
        InlineKeyboardButton(
            Fonts.smallcap(lang.lower()),
            callback_data=f"set_bahasa {inline_query.from_user.id} {lang}",
        )
        for lang in lang_code_translate
    ]
    buttons.add(*keyboard)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            InlineQueryResultArticle(
                title="Pilih Bahasa",
                input_message_content=InputTextMessageContent(
                    "<b>Silakan pilih bahasa untuk translate</b>"
                ),
                reply_markup=buttons,
            )
        ],
    )

async def set_bahasa_callback(client, callback_query):
    """Handle callback query for setting language."""
    data = callback_query.data.split()
    user_id = int(data[1])
    lang = data[2]
    client._translate[user_id] = {"negara": lang_code_translate[lang]}
    await callback_query.edit_message_text(
        f"<b>✅ Bahasa berhasil diubah ke:</b> {Fonts.smallcap(lang.lower())}"
    )


@DANTE.UBOT("tr|tl")
async def _(client, message):
    await tr_cmd(client, message)


@DANTE.UBOT("bahasa")
async def _(client, message):
    await set_lang_cmd(client, message)


@DANTE.INLINE("^ubah_bahasa")
async def _(client, inline_query):
    await ubah_bahasa_inline(client, inline_query)

@DANTE.UBOT("tts")
async def _(client, message):
    await tts_cmd(client, message)


@DANTE.CALLBACK("^set_bahasa")
async def _(client, callback_query):
    await set_bahasa_callback(client, callback_query)
