from pyrogram import Client, filters

# ---------------------------------------------------------
# Sesli Sohbet (Video Chat) Açıldığında Otomatik Bildirim
# ---------------------------------------------------------
@Client.on_message(filters.video_chat_started)
async def sesli_sohbet_acildi(client, message):
    bildirim_metni = (
        "▶️ 𝙲𝚊𝚗𝚕ı 𝚢𝚊𝚢ı𝚗 𝚋𝚊𝚜̧𝚕𝚊𝚍ı...\n\n"
        "ᴍᴀᴄ̧ ʏᴀʏıɴı ɪᴢʟᴇᴍᴇᴋ ɪᴄ̧ɪɴ.\n"
        "/yardim /tv kσmutlαrını kullαnαвílírsíníz..."
    )
    
    # Otomatik açılan servis mesajına yanıt olarak atar
    await message.reply_text(bildirim_metni)
