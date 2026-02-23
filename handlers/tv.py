import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# DİKKAT: Artık userbot'tan değil, ana main dosyasındaki RTMP motorunu çekiyoruz
from main import yayin_motoru

# Kanalları JSON dosyasından çeken fonksiyon
def kanallari_getir():
    dosya_yolu = "data/channels.json"
    if not os.path.exists(dosya_yolu):
        # Eğer senin data klasöründe değilse kök dizine bak
        dosya_yolu = "channels.json"
        
    if not os.path.exists(dosya_yolu):
        return {}
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return json.load(f)

# /tv Komutu
@Client.on_message(filters.command("tv") & filters.group)
async def tv_menusu(client, message):
    kanallar_sozlugu = kanallari_getir()
    if not kanallar_sozlugu:
        await message.reply_text("⚠️ Kanal listesi yüklenemedi!")
        return
    
    buton_listesi = []
    satir = []
    for kanal_adi in kanallar_sozlugu.keys():
        satir.append(InlineKeyboardButton(f"⊙ {kanal_adi} ⊙", callback_data=f"play_{kanal_adi}"))
        if len(satir) == 2:
            buton_listesi.append(satir)
            satir = []
    if satir: buton_listesi.append(satir)

    await message.reply_text(
        text="📺 **TV oynatmak için bir kanal seçin:**",
        reply_markup=InlineKeyboardMarkup(buton_listesi)
    )

# Kanal Seçildiğinde
@Client.on_callback_query(filters.regex(r"^play_(.*)"))
async def kanal_secildi(client, callback_query: CallbackQuery):
    kanal_ismi = callback_query.matches[0].group(1)
    talep_eden = callback_query.from_user.mention
    
    await callback_query.message.edit_text(text=f"📺 **{kanal_ismi}** başlatılıyor...\nTalep Eden: {talep_eden}")

    kanallar_sozlugu = kanallari_getir()
    yayin_linki = kanallar_sozlugu.get(kanal_ismi)

    if not yayin_linki:
        await callback_query.message.edit_text("❌ Link bulunamadı.")
        return

    # --- RTMP SİSTEMİ BURADA DEVREYE GİRİYOR ---
    # Artık chat_id gerekmiyor, doğrudan linki RTMP motoruna atıyoruz
    basarili_mi = await yayin_motoru.start_stream(yayin_linki)
    
    if basarili_mi:
        # Başarılı metni
        basarili_metni = (
            "𝙲𝚊𝚗𝚕ı 𝚢𝚊𝚢ı𝚗 𝚋𝚊𝚜̧𝚕𝚊𝚍ı | ♬\n\n"
            f" **{kanal_ismi}**\n"
            "✯Cαɳʅı Yαყıɳ | 🇹🇷 | 🇦🇿\n\n"
            "💡 _Yayın 80 dakikada bir otomatik yenilenecektir._"
        )
        butonlar = InlineKeyboardMarkup([[InlineKeyboardButton("📺 Kanal Listesi", callback_data="tv_kanal_listesi")]])
        await callback_query.message.edit_text(text=basarili_metni, reply_markup=butonlar)
    else:
        await callback_query.message.edit_text("❌ Yayın başlatılamadı. RTMP/FFmpeg hatası.")

# Kanal Listesi Butonu (Geri Dönüş)
@Client.on_callback_query(filters.regex("^tv_kanal_listesi$"))
async def kanal_listesi_buton(client, callback_query: CallbackQuery):
    # Ana menü kodunu buraya tekrar çağırıyoruz
    await tv_menusu(client, callback_query.message)
