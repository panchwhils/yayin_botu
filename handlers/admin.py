import os
import json
from pyrogram import Client, filters
from dotenv import load_dotenv

# .env dosyasındaki SAHIP_ID'yi çekiyoruz
load_dotenv()
SAHIP_ID = int(os.getenv("SAHIP_ID", 0)) # .env dosyana SAHIP_ID=123456789 şeklinde kendi ID'ni eklemelisin

AUTH_DOSYASI = "data/auth.json"

# Yardımcı Fonksiyon: Yetkili listesini okur
def auth_listesini_getir():
    if not os.path.exists(AUTH_DOSYASI):
        return []
    with open(AUTH_DOSYASI, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Yardımcı Fonksiyon: Yetkili listesini kaydeder
def auth_listesini_kaydet(liste):
    with open(AUTH_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(liste, f, indent=4)

# Komutun kime uygulandığını (yanıtlama veya etiketleme) bulan fonksiyon
async def hedef_kullaniciyi_bul(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            return await client.get_users(message.command[1])
        except:
            return None
    return None

# ---------------------------------------------------------
# /auth Komutu - Kullanıcıyı Yetkilendirir (Sadece SAHIP_ID kullanabilir)
# ---------------------------------------------------------
@Client.on_message(filters.command("auth") & filters.user(SAHIP_ID))
async def yetki_ver(client, message):
    hedef_kullanici = await hedef_kullaniciyi_bul(client, message)
    
    if not hedef_kullanici:
        await message.reply_text("Lütfen bir kullanıcıyı yanıtlayın veya ID/Kullanıcı adı girin.")
        return

    auth_listesi = auth_listesini_getir()
    
    if hedef_kullanici.id in auth_listesi:
        await message.reply_text(f"{hedef_kullanici.mention} zaten yetkili listesinde bulunuyor.")
        return
        
    auth_listesi.append(hedef_kullanici.id)
    auth_listesini_kaydet(auth_listesi)
    
    await message.reply_text(f"{hedef_kullanici.mention} yetkili kullanıcılar listesine eklendi.")

# ---------------------------------------------------------
# /unauth Komutu - Kullanıcının Yetkisini Alır (Sadece SAHIP_ID kullanabilir)
# ---------------------------------------------------------
@Client.on_message(filters.command("unauth") & filters.user(SAHIP_ID))
async def yetki_al(client, message):
    hedef_kullanici = await hedef_kullaniciyi_bul(client, message)
    
    if not hedef_kullanici:
        await message.reply_text("Lütfen bir kullanıcıyı yanıtlayın veya ID/Kullanıcı adı girin.")
        return

    auth_listesi = auth_listesini_getir()
    
    if hedef_kullanici.id not in auth_listesi:
        await message.reply_text(f"{hedef_kullanici.mention} yetkili listesinde değil.")
        return
        
    auth_listesi.remove(hedef_kullanici.id)
    auth_listesini_kaydet(auth_listesi)
    
    await message.reply_text(f"{hedef_kullanici.mention} yetkili kullanıcılar listesinden kaldırıldı.")

# ---------------------------------------------------------
# /authliste Komutu - Yetkili Kullanıcıları Listeler
# ---------------------------------------------------------
@Client.on_message(filters.command("authliste"))
async def yetkili_listesi(client, message):
    auth_listesi = auth_listesini_getir()
    
    if not auth_listesi:
        await message.reply_text("Yetkili kullanıcılar listesi şu an boş.")
        return
        
    mesaj = "Yetkili kullanıcılar listesi 👑\n\n"
    
    for user_id in auth_listesi:
        try:
            # ID'yi alıp Telegram'dan kullanıcının güncel adını/etiketini çekiyoruz
            user = await client.get_users(user_id)
            mesaj += f"• {user.mention}\n"
        except:
            # Eğer kullanıcı hesabını sildiyse ID olarak görünür
            mesaj += f"• `{user_id}`\n"
            
    await message.reply_text(mesaj)
