from asyncio import QueueEmpty
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate, GroupCallParticipant, MediaStream, Update, StreamAudioEnded
from DanteUserbot import *

@ubot.pytgcalls_decorator()
async def clear_chat_queue(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)

@ubot.pytgcalls_decorator()
async def stream_end_handler(client, update: Update):
    if isinstance(update, GroupCallParticipant):
        print(update)
    elif isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        print(f"Stream ended for chat_id: {chat_id}")
        op = await skip_current_song(client, chat_id)
        if op == 1:
            await client.send_message(chat_id, "`Queue is Empty, Leaving Voice Chat...`")
            await client.leave_call(chat_id)
        elif op == 2:
            await client.send_message(chat_id, "**Some Error Occurred** \n`Clearing the Queues and Leaving the Voice Chat...`")
            await client.leave_call(chat_id)
        else:
            await client.send_message(chat_id, f"**🎧 Now Playing** \n[{op[0]}]({op[1]}) | `{op[2]}`", disable_web_page_preview=True)
    else:
        print(f"Unhandled update type: {type(update)}")
        pass
