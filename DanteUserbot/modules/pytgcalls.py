from asyncio import QueueEmpty
from pytgcalls import GroupCallFactory
from pytgcalls.implementation.group_call_file import GroupCallFileAction
from pytgcalls.implementation.group_call import GroupCallAction
from DanteUserbot import *

# Initialize GroupCallFactory
group_call_factory = GroupCallFactory(ubot)
if not hasattr(ubot, "call_py"):
    ubot.call_py = group_call_factory.get_file_group_call()

async def handle_playout_ended(chat_id: int):
    print(f"Playout ended for chat_id: {chat_id}")
    op = await skip_current_song(ubot, chat_id)
    if op == 1:
        await ubot.send_message(chat_id, "`Queue is Empty, Leaving Voice Chat...`")
        await ubot.call_py.leave_group_call(chat_id)
    elif op == 2:
        await ubot.send_message(chat_id, "**Some Error Occurred** \n`Clearing the Queues and Leaving the Voice Chat...`")
        await ubot.call_py.leave_group_call(chat_id)
    else:
        await ubot.send_message(chat_id, f"**🎧 Now Playing** \n[{op[0]}]({op[1]}) | `{op[2]}`", disable_web_page_preview=True)

# Monitor playout ended events
ubot.call_py.on_playout_ended = handle_playout_ended
