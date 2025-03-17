async def tanya(client, text):
    url = "https://itzpire.com/ai/botika"
    params = {
        "q": f"{text}",
        "user": f"{client, text.me.first_name}",
        "model": "sindy"
    }
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        msg = data["result"]
        return f"<blockquote>{msg}</blockquote>"
    else:
        return "Server error"

@HIRO.UBOT("ask")
async def gtp(client, message: Message):
    text = get_text(message)
    if not text:
        return await message.reply("perintah anda salah, gunakan .ask pertanyaan")
    pros = await message.reply("menjawab..")
    hasil = await tanya(client, text)
    return await pros.edit(hasil)