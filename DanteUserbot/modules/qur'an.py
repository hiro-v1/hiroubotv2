import requests
import wget
from pyrogram import *

processed_surah_numbers = set()

from DanteUserbot import *


def download_audio(url, file_name):
    try:
        wget.download(url, file_name)
        return True
    except Exception as e:
        print(f"Failed to download audio: {e}")
        return False


def ambil_nama_surah(surah_name):
    response = requests.get("https://equran.id/api/v2/surat")
    if response.status_code == 200:
        surah_list = response.json()["data"]
        for surah_info in surah_list:
            if surah_info["namaLatin"].lower() == surah_name.lower():
                return surah_info
    return None


def ambil_daftar_surah():
    response = requests.get("https://equran.id/api/v2/surat")
    surah_list = []
    if response.status_code == 200:
        data = response.json()["data"]
        for surah_info in data:
            surah_list.append(
                (
                    surah_info["nomor"],
                    surah_info["namaLatin"],
                    surah_info["jumlahAyat"],
                    surah_info["tempatTurun"],
                )
            )
    return surah_list


@DANTE.UBOT("listsurah")
async def listsurah(client, message):
    pros = await message.reply("proses")
    msg = f"<b>Nama Surah, Jumlah Ayat, Tempat Surah Turun</b>:\n\n"
    for count, nama, jumlah, turun in ambil_daftar_surah():
        msg += f"<b>• {count}</b>. <b>{nama}</b> <code>{jumlah}</code> <b>{turun}</b>\n"
    await message.reply(msg, reply_to_message_id=ReplyCheck(message))
    await pros.delete()
    return


@DANTE.UBOT("surah")
async def surah(client, message):
    pros = await message.reply("proses")

    surah_name = (
        message.text.split(maxsplit=1)[1].strip().lower() if len(message.command) > 1 else None
    )

    if not surah_name:
        await message.reply("Silahkan berikan nama surah. contoh `surah Al-Ma'un`")
        await pros.delete()
        return

    surah_info = ambil_nama_surah(surah_name)

    if surah_info:
        response_text = (
            f"**Nomor Surah**: `{surah_info['nomor']}`\n"
            f"**Nama Surah**: `{surah_info['nama']}`\n"
            f"**Nama Surah (Latin)**: `{surah_info['namaLatin']}`\n"
            f"**Jumlah Ayat**: `{surah_info['jumlahAyat']}`\n"
            f"**Tempat Turun**: `{surah_info['tempatTurun']}`\n"
            f"**Arti**: `{surah_info['arti']}`\n"
            f"**Deskripsi**: `{surah_info['deskripsi']}`\n"
        )

        audio_urls = surah_info["audioFull"]
        qori_name = None
        for key, url in audio_urls.items():
            if url:
                qori_name = url.split("audio-full/")[1].split("/")[0]
                break

        response_text += f"**Qori**: `{qori_name}`\n" if qori_name else ""
        audio_url = next((url for url in audio_urls.values() if url), None)
        if audio_url:
            audio_file_name = f"{surah_name.capitalize()}.mp3"
            if download_audio(audio_url, audio_file_name):
                if len(response_text) > 4096:
                    file_name = f"{surah_name.capitalize()}.txt"
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(response_text)
                    aud = await message.reply_audio(
                        audio_file_name, reply_to_message_id=ReplyCheck(message)
                    )
                    await message.reply_document(file_name, reply_to_message_id=aud.id)
                else:
                    await message.reply_audio(
                        audio_file_name,
                        caption=response_text,
                        reply_to_message_id=ReplyCheck(message),
                    )
            else:
                await message.reply("Gagal mengunduh audio.")
        else:
            await message.reply(response_text, reply_to_message_id=ReplyCheck(message))

        await pros.delete()
        return
    else:
        await message.reply("Surah dengan nama 'tersebut' tidak ditemukan. gunakan listsurah")
        await pros.delete()
        return
