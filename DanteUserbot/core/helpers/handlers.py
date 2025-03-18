from DanteUserbot import *
from pytgcalls import GroupCallFactory
from pytgcalls.types import GroupCallType  # Perbaikan impor
from DanteUserbot.core.helpers.queues import *

# Replace MediaStream usage with GroupCallFactory methods
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
                media_type = chat_queue[1][3]
                quality = chat_queue[1][4]

                group_call = GroupCallFactory(client).get(GroupCallType.RAW)  # Menggunakan metode yang benar

                if media_type == "Audio":
                    await group_call.start_audio_stream(
                        input_filename=url,  # File audio dari URL
                        output_filename=None,  # Tidak perlu output jika hanya streaming
                        play_on_repeat=False
                    )

                elif media_type == "Video":
                    await group_call.start_video_stream(
                        input_filename=url,
                        output_filename=None,
                        play_on_repeat=False
                    )

                pop_an_item(chat_id)
                return [songname, link, media_type]

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
