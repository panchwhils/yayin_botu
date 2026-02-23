import subprocess

# Test edilecek link (Senin linklerden biri)
link = "http://tr3.153689.xyz:80/AnsUcxM9zY/JSZnByRJrm/873521"

# FFmpeg'i manuel çalıştırıp loglarına bakacağız
komut = [
    "ffmpeg",
    "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "-i", link,
    "-t", "5",  # 5 saniye dene
    "-f", "null", "-"
]

print("⏳ Link test ediliyor...")
sonuc = subprocess.run(komut, stderr=subprocess.PIPE, text=True)

if "Server returned 403 Forbidden" in sonuc.stderr:
    print("❌ HATA: 403 Yasaklandı! (Link, sunucu IP'sini engelliyor veya Token süresi dolmuş)")
elif "Connection refused" in sonuc.stderr:
    print("❌ HATA: Bağlantı reddedildi! (Link ölü)")
elif "Duration" in sonuc.stderr:
    print("✅ BAŞARILI! Sunucu bu linki açabiliyor. Sorun bot kodlarında.")
else:
    print("❌ BİLİNMEYEN HATA. İşte FFmpeg çıktısı:")
    print(sonuc.stderr)
