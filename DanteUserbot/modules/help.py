from DanteUserbot import *
import re
from importlib import import_module
from pyrogram.types import *
from DanteUserbot.core.function.emoji import emoji
from DanteUserbot.core.helpers.client import DANTE

@DANTE.UBOT("help")
async def help_cmd(client, message):
    if not get_arg(message):
        try:
            x = await client.get_inline_bot_results(bot.me.username, "user_help")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await message.reply(f"⚠️ Terjadi kesalahan:\n<code>{error}</code>")
    else:
        module = get_arg(message)
        if module in HELP_COMMANDS:
            await message.reply(
                HELP_COMMANDS[module].HELP,
                quote=True,
                disable_web_page_preview=True,
            )
        else:
            await message.reply(
                f"<blockquote><b>❌ Tidak dapat ditemukan modul dengan nama <code>{module}</code></b></blockquote>"
            )

@DANTE.INLINE("^user_help")
async def menu_inline(client, inline_query):
    """Handle inline query for help menu."""
    prefix = await ubot.get_prefix(inline_query.from_user.id)
    msg = f"<b>❏ Help Menu\n├ Prefix: {' '.join(prefix)}\n╰ Commands: {len(HELP_COMMANDS)}</b>"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=60,
        results=[
            InlineQueryResultArticle(
                title="Help Menu",
                input_message_content=InputTextMessageContent(msg),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELP_COMMANDS, "help")
                ),
            )
        ],
    )

@DANTE.CALLBACK("^help_(.*?)")
async def menu_callback(client, callback_query):
    """Handle callback query for help navigation."""
    match = re.match(r"help_(module|prev|next|back)(?:\((.+?)\))?", callback_query.data)
    if not match:
        return

    action, module = match.groups()
    prefix = await ubot.get_prefix(callback_query.from_user.id)
    top_text = f"<b>❏ Help Menu\n├ Prefix: {' '.join(prefix)}\n╰ Commands: {len(HELP_COMMANDS)}</b>"

    if action == "module":
        text = HELP_COMMANDS[module].__HELP__.format(next(iter(prefix)))
        buttons = [[InlineKeyboardButton("🔙 Kembali", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    elif action in {"prev", "next"}:
        curr_page = int(module)
        new_page = curr_page - 1 if action == "prev" else curr_page + 1
        await callback_query.edit_message_text(
            top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(new_page, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
    elif action == "back":
        await callback_query.edit_message_text(
            top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
