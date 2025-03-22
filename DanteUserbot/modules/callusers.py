from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from DanteUserbot import OWNER_ID, bot
from DanteUserbot.core.helpers.clalluser import get_all_users
from DanteUserbot.core.helpers.client import DANTE  # Import custom decorators

# Command to initiate the broadcast process
@DANTE.OWNER
async def broadcast_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Broad", callback_data="start_broadcast")]]
    )
    await message.reply("Apa yang ingin anda sampaikan?", reply_markup=keyboard)

# Callback query handler for broadcast options
@DANTE.CALLBACK("start_broadcast")
async def start_broadcast(client: Client, callback_query):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Kirim Pesan", callback_data="send_message")],
            [InlineKeyboardButton("Batal", callback_data="cancel_broadcast")]
        ]
    )
    await callback_query.message.edit_text("Apa yang ingin anda sampaikan?", reply_markup=keyboard)

# Callback query handler for sending message
@DANTE.CALLBACK("send_message")
async def send_message(client: Client, callback_query):
    await callback_query.message.edit_text("Silakan kirim pesan yang ingin anda sampaikan.")
    bot.register_next_step_handler(callback_query.message, broadcast_message)

async def broadcast_message(message: Message):
    users = await get_all_users()
    for user in users:
        try:
            await bot.send_message(user.id, message.text)
        except Exception as e:
            print(f"❌ Gagal mengirim pesan ke {user.id}: {e}")
    await message.reply("Broadcast selesai.")

# Callback query handler for canceling broadcast
@DANTE.CALLBACK("cancel_broadcast")
async def cancel_broadcast(client: Client, callback_query):
    await callback_query.message.edit_text("Broadcast dibatalkan.")

# Handle incoming messages from users
@DANTE.PRIVATE
async def handle_user_message(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Balas", callback_data=f"reply_{message.from_user.id}")],
            [InlineKeyboardButton("Hapus", callback_data=f"delete_{message.id}")]
        ]
    )
    await message.reply("ADA PESAN MASUK\n\n" + message.text, reply_markup=keyboard)

# Handle reply from owner to user
@DANTE.CALLBACK(r"reply_(\d+)")
async def reply_to_user(client: Client, callback_query):
    user_id = int(callback_query.data.split("_")[1])
    await callback_query.message.edit_text("Silakan ketik balasan anda.")
    bot.register_next_step_handler(callback_query.message, send_reply, user_id)

async def send_reply(message: Message, user_id: int):
    await bot.send_message(user_id, message.text)
    await message.reply("Pesan balasan anda telah dikirim, mohon tunggu.")

# Handle delete message
@DANTE.CALLBACK(r"delete_(\d+)")
async def delete_message(client: Client, callback_query):
    message_id = int(callback_query.data.split("_")[1])
    await bot.delete_messages(callback_query.message.chat.id, message_id)
    await callback_query.message.edit_text("Pesan telah dihapus.")
