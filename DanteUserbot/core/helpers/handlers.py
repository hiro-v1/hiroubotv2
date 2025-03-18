from DanteUserbot import *
from pytgcalls import GroupCallFactory
from pytgcalls.stream import MediaStream  # Updated import path for MediaStream
from pytgcalls.types.stream import VideoQuality, AudioQuality  # Corrected import paths
from DanteUserbot.core.helpers.queues import *

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
                            VideoQuality.HIGH,
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
