async def eor(event, text):
    if event.reply_to_msg_id:
        return await event.reply(text)
    return await event.edit(text)
