from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from DanteUserbot import *
from pytgcalls.exceptions import NotInCallError

async def lanjut_current_song(client, chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            try:
                await client.call_py.leave_call(chat_id)
            except NotInCallError:
                pass
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
                    await client.call_py.play(
                        chat_id,
                        MediaStream(
                            url,
                            AudioQuality.STUDIO,
                        ),
                    )
                elif type == "Video":
                    await client.call_py.play(
                        chat_id,
                        MediaStream(
                            url,
                        ),
                    )
                pop_an_item(chat_id)
                return [songname, link, type]
            except:
                await client.call_py.leave_call(chat_id)
                clear_queue(chat_id)
                return 2
    else:
        return 0

@DANTE.UBOT("skip")
@DANTE.GROUP
async def skip(client, m: Message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await lanjut_current_song(client, chat_id)
        if op == 0:
            await m.reply(f"{ggl}<b>Nothing Is Playing</b>")
        elif op == 1:
            await m.reply(f"{ggl}<b>Queue is Empty, Leaving Voice Chat...</b>")
        elif op == 2:
            await m.reply(f"{ggl}<b>Some Error Occurred</b> \n<b>Clearing the Queues and Leaving the Voice Chat...</b>")
        else:
            await m.reply(f"**<emoji id=6005994005148471369>⏩</emoji> Skipped** \n**<emoji id=5895705279416241926>▶</emoji> Now Playing** - [{op[0]}]({op[1]}) | `{op[2]}`", disable_web_page_preview=True)

    else:
        skip = m.text.split(None, 1)[1]
        OP = "**Removed the following songs from Queue:-**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)        

@DANTE.UBOT("end")
@DANTE.GROUP
async def stop(client, m: Message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await client.call_py.leave_call(chat_id)
            clear_queue(chat_id)
            await m.reply(f"{brhsl}<b>Streaming Ended !</b>")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply(f"{ggl}<b>Nothing is Streaming</b>")
   
@DANTE.UBOT("pause")
@DANTE.GROUP
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await client.call_py.pause_stream(chat_id)
            await m.reply("<b><emoji id=6005824650293022970>⏸️</emoji> Paused Streaming</b>")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("`Nothing is Streaming`")
      
@DANTE.UBOT("resume")
@DANTE.GROUP
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await client.call_py.resume_stream(chat_id)
            await m.reply("**<emoji id=5895705279416241926>▶</emoji> Resumed Streaming**")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("`Nothing is Streaming`")
