import os
from pyrogram import Client
from dotenv import load_dotenv
from core.stream_bridge import StreamBridge

# .env dosyasındaki bilgileri yüklüyoruz
load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

if not SESSION_STRING:
    print("⚠️ UYARI: .env dosyasında SESSION_STRING bulunamadı! Yayın özelliği çalışmayacak.")

# Userbot istemcisi (Yayını kanallara/gruplara basacak olan asıl hesap)
user_app = Client(
    "yayin_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Yayın köprümüzü Userbot ile birleştirip hazır hale getiriyoruz
yayin_motoru = StreamBridge(user_app)
