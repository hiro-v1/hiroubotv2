import io
import os

import google.generativeai as genai
from pyrogram.enums import ChatAction
from pyrogram.errors import *

from DanteUserbot import *

genai.configure(api_key="AIzaSyBw_hspHrlcySkIsa9Qx5zA7PqKAyCwwPs")


def gemini(text):
    try:
        generation_config = {
            "temperature": 0.6,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
        ]
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        respon = model.generate_content(text)
        if respon:
            return f"{respon.text}"
    except Exception as e:
        return f"Error generating text: {str(e)}"


@DANTE.UBOT("gemini")
async def gemini(client, message):
    pros = await message.reply("proses")
    reply_text = client.get_text(message)
    if not reply_text:
        return pros.edit("terjadi kesalahan") 
    try:
        chat_id = message.chat.id
        if message.sender_chat:
            message.sender_chat.id
        else:
            message.from_user.id
        respon = gemini(query)
        await message._client.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(2)
        if len(respon) > 2550:
            with open("chatbot.txt", "wb") as file:
                file.write(respon.encode("utf-8"))
            await message._client.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
            await asyncio.sleep(2)
            await message._client.send_document(
                chat_id, "chatbot.txt", reply_to_message_id=message.id
            )
            os.remove("chatbot.txt")
            return await message._client.send_chat_action(chat_id, ChatAction.CANCEL)
        else:
            await message.reply_text(
                "{} {}", reply_to_message_id=message.id
            )
        return await message._client.send_chat_action(chat_id, ChatAction.CANCEL)
    except ChatWriteForbidden:
        return

# @DANTE.UBOT("gemini")
# async def gemini(client, message):
#    pros = await message.reply("proses")
#    reply_text = client.get_text(message)
#    if not reply_text:
#        return pros.edit("terjadi kesalahan")
#   await mari_kirim()
#    return await pros.delete()
chat_topics = {}

async def costum_api(client, text, user_id):
    if user_id in chat_topics:
        topik = chat_topics[user_id]
    else:
        topik = text
        chat_topics[user_id] = topik

    gw = f"<a href=tg://user?id={c.me.id}>{client.me.first_name} {client.me.last_name or ''}</a>"
    bahan = [
        {
            "role": "system",
            "content": f"Lo adalah asisten telegram dari pengguna akun {gw}",
        },
        {
            "role": "assistant",
            "content": f"Lo adalah asisten telegram dari pengguna akun {gw} gunakan bahasa Indonesia toxic lo gw, anj, mmg, kntl, bacot serta gausah sok asik dan gausah menjelaskan apapun tugas lo hanya membalas pesan dengan singkat.",
        },
        {"role": "user", "content": f"{topik}"},
    ]
    url = "https://api.botcahx.eu.org/api/search/openai-custom"
    payload = {"message": bahan, "apikey": "bee"}
    res = await fetch.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["result"]
    else:
        return f"{res.text}"


@DANTE.UBOT("pertanyaan")
async def pertanyaan(client, message):
    a = client.get_text(message)
    user_id = client.me.id
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    prs = await message.reply_text("proses")

    try:
        x = await costum_api(client, a, user_id)
        chat_topics[user_id] = a
        await prs.delete()
        return await message.reply(
            "{} {}", reply_to_message_id=message.id
        )
    except Exception as e:
        await prs.delete()
        return await message.reply("err")


async def generate_real(client, text):
    url = f"https://itzpire.com/ai/realistic?prompt={text}"
    res = await fetch.get(url)
    if res.status_code == 200:
        data = res.json()
        file = data["result"]
        photo = f"iz_{client.me.id}.jpg"
        await client.bash(f"wget {file} -O {photo}")
        return photo


@DANTE.UBOT("fluxai")
async def xai(client, message):
    pros = await message.reply("proses")
    text = client.get_arg(message)
    if not text:
        return pros.edit("proses...")
    try:
        image = await generate_real(client, text)
        await message.reply_photo(image)
        if os.path.exists(image):
            os.remove(image)
        return await pros.delete()
    except ImageProcessFailed as e:
        await message.reply("err")
        return await pros.delete()


async def _(client, message):
    pros = await message.reply("proses")
    text = client.get_arg(message)
    if not text:
        return pros.edit("bot terjadi kesalahan dalam memanggil")
    data = {"string": f"{text}"}
    head = {"accept": "image/jpeg"}
    url = f"https://widipe.com/v1/text2img?text={data}"
    res = await fetch.get(url, headers=head)
    image_data = res.read()
    image = io.BytesIO(image_data)
    image.name = f"{client.me.id}.jpg"
    try:
        await message.reply_photo(image)
        if os.path.exists(f"{c.me.id}.jpg"):
            os.remove(f"{client.me.id}.jpg")
        return await pros.delete()
    except ImageProcessFailed as e:
        await message.reply("err")
        return await pros.delete()
