import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# İzinli grupları JSON dosyasından kontrol eden yardımcı fonksiyon
def grup_izinli_mi(chat_id):
    dosya_yolu = "data/izinli_gruplar.json"
    
    # Dosya yoksa veya boşsa kimseye izin verme
    if not os.path.exists(dosya_yolu):
        return False
        
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            izinli_gruplar = json.load(f)
            # Eğer grubun ID'si listede varsa True (İzinli), yoksa False (İzinsiz) döner
            return chat_id in izinli_gruplar
    except:
        return False

# Bota yeni biri eklendiğinde (veya bot bir gruba eklendiğinde) çalışır
@Client.on_message(filters.new_chat_members)
async def gruba_eklenme_kontrolu(client, message):
    bot_bilgisi = await client.get_me()
    
    # Gruba eklenen kişiler arasında botun kendisi var mı diye bakıyoruz
    bot_eklendi_mi = any(uye.id == bot_bilgisi.id for uye in message.new_chat_members)
            
    if bot_eklendi_mi:
        chat_id = message.chat.id
        
        # Grubun izni YOKSA çalışacak kısım
        if not grup_izinli_mi(chat_id):
            
            uyari_metni = (
                "⚠️ Merhaba! Botu Sadece İzinli Gruplar ve Kanallar kullanabilir\n\n"
                "✅ İzin İçin Sahip ile iletişime geçiniz.\n"
                "İzin verilmediği için otomatik olarak ayrılıyorum. 👋"
            )
            
            # .env dosyasından destek linkini alıyoruz
            destek_link = os.getenv("DESTEK_ID", "https://t.me/destek")
            
            destek_butonu = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("👨‍💻 Destek", url=destek_link)]
                ]
            )
            
            # Uyarı mesajını ve butonu gruba atıyoruz
            await message.reply_text(text=uyari_metni, reply_markup=destek_butonu)
            
            # Mesajın okunması için 2 saniye bekleyip gruptan ayrılıyoruz
            await asyncio.sleep(2)
            await client.leave_chat(chat_id)
            print(f"🚫 İzinsiz gruba eklendim ve çıktım. Grup ID: {chat_id}")
        else:
            print(f"✅ İzinli gruba eklendim. Grup ID: {chat_id}")
