from DanteUserbot import *
from pytgcalls import GroupCallFactory
from pytgcalls.types import StreamType  # Sesuai dengan versi terbaru
from pytgcalls.types.stream import VideoQuality, AudioQuality  # Perbaikan import
from DanteUserbot.core.helpers.queues import *

async def skip_current_song(client, chat_id):
    """Melewati lagu saat ini dan memainkan lagu berikutnya dalam antrean."""
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await client.leave_call(chat_id)
            clear_queue(chat_id)
            return 1  # Tidak ada lagi lagu dalam antrean
        else:
            try:
                songname, url, link, type, Q = chat_queue[1]

                if type == "Audio":
                    await client.play(
                        chat_id,
                        StreamType().local_stream(url, AudioQuality.STUDIO)  # Perbaikan sintaks
                    )
                elif type == "Video":
                    await client.play(
                        chat_id,
                        StreamType().local_stream(url, VideoQuality.HIGH)  # Perbaikan sintaks
                    )

                pop_an_item(chat_id)  # Hapus lagu yang sudah selesai
                return [songname, link, type]
            except Exception as e:
                print(f"❌ Error di skip_current_song: {e}")
                await client.leave_call(chat_id)
                clear_queue(chat_id)
                return 2  # Terjadi error, semua lagu dihentikan
    else:
        return 0  # Tidak ada antrean aktif

async def skip_item(chat_id, index):
    """Melewati lagu tertentu dalam antrean berdasarkan indeks."""
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            index = int(index)
            songname = chat_queue[index][0]
            chat_queue.pop(index)  # Hapus lagu dari antrean
            return songname
        except Exception as e:
            print(f"❌ Error di skip_item: {e}")
            return 0  # Gagal menghapus lagu
    else:
        return 0  # Tidak ada antrean aktif
