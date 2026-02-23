import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Metnimiz her iki yerde de (komut ve buton) kullanılacağı için yukarıya sabitliyoruz
YARDIM_METNI = (
    "**Bot Komutları ve Özellikleri**\n\n"
    "/tv - 📺 Grupta TV yayını başlatır.\n"
    "/yardim - Yardım menüsünü gösterir.\n"
    "/authliste - İzinli Kullanıcı listesi\n\n"
    "Herhangi bir sorun olursa destek yazın."
)

# Butonlarımızı oluşturan fonksiyon
def yardim_butonlari():
    destek_link = os.getenv("DESTEK_ID", "https://t.me/destek") 
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👨‍💻 Destek", url=destek_link),
                InlineKeyboardButton("❌ Kapat", callback_data="mesaji_kapat")
            ]
        ]
    )

# 1. Kullanıcı sohbete /yardim yazdığında çalışacak kısım
@Client.on_message(filters.command(["yardim", "help"]))
async def yardim_komutu(client, message):
    await message.reply_text(
        text=YARDIM_METNI,
        reply_markup=yardim_butonlari()
    )

# 2. Start menüsündeki "Yardım ve Komutlar" butonuna basıldığında çalışacak kısım
@Client.on_callback_query(filters.regex("^yardim_menu$"))
async def yardim_menu_callback(client, callback_query: CallbackQuery):
    # Yeni mesaj atmak yerine mevcut mesajı yardım metni ile güncelliyoruz
    await callback_query.message.edit_text(
        text=YARDIM_METNI,
        reply_markup=yardim_butonlari()
    )

# 3. "Kapat" butonuna basıldığında mesajı silecek kısım
@Client.on_callback_query(filters.regex("^mesaji_kapat$"))
async def kapat_callback(client, callback_query: CallbackQuery):
    await callback_query.message.delete()
