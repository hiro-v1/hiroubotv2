from asyncio import QueueEmpty
from pytgcalls import GroupCallFactory
from pytgcalls.implementation.group_call_file import GroupCallFileAction
from pytgcalls.implementation.group_call import GroupCallAction
from DanteUserbot import *

# Initialize GroupCallFactory
group_call_factory = GroupCallFactory(ubot)
if not hasattr(ubot, "call_py"):
    ubot.call_py = group_call_factory.get_file_group_call()

@ubot.call_py.on_network_status_changed
async def clear_chat_queue(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)

@ubot.call_py.on_stream_end
async def stream_end_handler(client, chat_id: int):
    print(f"Stream ended for chat_id: {chat_id}")
    op = await skip_current_song(client, chat_id)
    if op == 1:
        await client.send_message(chat_id, "`Queue is Empty, Leaving Voice Chat...`")
        await ubot.call_py.leave_group_call(chat_id)
    elif op == 2:
        await client.send_message(chat_id, "**Some Error Occurred** \n`Clearing the Queues and Leaving the Voice Chat...`")
        await ubot.call_py.leave_group_call(chat_id)
    else:
        await client.send_message(chat_id, f"**🎧 Now Playing** \n[{op[0]}]({op[1]}) | `{op[2]}`", disable_web_page_preview=True)
