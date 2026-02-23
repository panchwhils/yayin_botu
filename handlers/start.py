import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start_komutu(client, message):
    # Kullanıcının adını alıyoruz ({} yerine geçecek)
    kullanici_adi = message.from_user.first_name
    
    # Senin hazırladığın karşılama metni
    start_metni = (
        f"Merhaba {kullanici_adi},\n"
        "Ben 𝐍𝐨𝐭𝐚𝐥𝐚𝐫 𝐌𝐚𝐜̧ 𝐈̇𝐳𝐥𝐞𝐦𝐞 🇹🇷 !\n\n"
        "Bazı harika ve kullanışlı özelliklere sahip bir Maç izleme botu.\n\n"
        "Daha fazla bilgi için yardım butonuna tıkla."
    )
    
    # .env dosyasından destek ve kanal linklerini çekiyoruz
    destek_link = os.getenv("DESTEK_ID", "https://t.me/destek") 
    kanal_link = os.getenv("KANAL_LINK", "https://t.me/kanal")
    
    # Botun kendi kullanıcı adını alıyoruz (Gruba ekle butonu için lazım)
    bot_bilgisi = await client.get_me()
    bot_username = bot_bilgisi.username
    
    # İstediğin 4 butonun dizilimi
    butonlar = InlineKeyboardMarkup(
        [
            [
                # Bu buton direkt botu bir gruba ekleme ekranını açar
                InlineKeyboardButton("➕ Beni Gruba Ekle", url=f"https://t.me/{bot_username}?startgroup=true")
            ],
            [
                InlineKeyboardButton("ℹ️ Yardım ve Komutlar", callback_data="yardim_menu")
            ],
            [
                InlineKeyboardButton("👨‍💻 Destek", url=destek_link),
                InlineKeyboardButton("📢 Kanal", url=kanal_link)
            ]
        ]
    )
    
    # Mesajı ve butonları gönderiyoruz
    await message.reply_text(
        text=start_metni,
        reply_markup=butonlar
    )
