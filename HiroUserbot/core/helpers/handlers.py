from HiroUserbot import *
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate, GroupCallParticipant, MediaStream, Update, VideoQuality, AudioQuality, ChatUpdate
from pytgcalls.types import StreamAudioEnded
from HiroUserbot.core.helpers.queues import *

async def skip_current_song(client, chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await client.leave_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            try:
                songname = chat_queue[1][0]
                url = chat_queue[1][1]
                link = chat_queue[1][2]
                type = chat_queue[1][3]
                Q = chat_queue[1][4]
                if type == "Audio":
                    await client.play(
                        chat_id,
                        MediaStream(
                            url,
                            AudioQuality.STUDIO,
                        ),
                    )
                elif type == "Video":
                    await client.play(
                        chat_id,
                        MediaStream(
                            url,
                        ),
                    )
                pop_an_item(chat_id)
                return [songname, link, type]
            except Exception as e:
                print(f"Error in skip_current_song: {e}")
                await client.leave_call(chat_id)
                clear_queue(chat_id)
                return 2
    else:
        return 0

async def skip_item(chat_id, h):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(h)
            songname = chat_queue[x][0]
            chat_queue.pop(x)
            return songname
        except Exception as e:
            print(e)
            return 0
    else:
        return 0
