EMO = {
    "bintang": "<emoji id=5911461474315802019>⭐</emoji>",
    "loading": "<emoji id=5801044672658805468>✨</emoji>",
    "proses": "<emoji id=6276248783525251352>🔄</emoji>",
    "gagal": "<emoji id=6278161560095426411>❌</emoji>",
    "done": "<emoji id=6278555627639801385>✅</emoji>",
    "upload": "<emoji id=5911100572508885928>♻️</emoji>",
    "berhasil": "<emoji id=6278555627639801385>✅</emoji>",
    "ping": "<emoji id=5801044672658805468>✨</emoji>",
    "mention": "<emoji id=5911461474315802019>⭐</emoji>",
    "ubot": "<emoji id=5911100572508885928>♻️</emoji>",
}

def emoji(alias):
    """Mendapatkan emoji berdasarkan alias dengan fallback jika tidak ditemukan."""
    return EMO.get(alias, "Emoji tidak ditemukan.")
