import subprocess

# Senin Bein Sports linklerinden birini buraya yapıştır
link = "http://tr3.153689.xyz:80/AnsUcxM9zY/JSZnByRJrm/873521"

komut = [
    "ffmpeg", 
    "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "-i", link,
    "-t", "5", # Sadece 5 saniye dene
    "-f", "null", "-"
]

print("⏳ FFmpeg testi yapılıyor...")
try:
    process = subprocess.run(komut, stderr=subprocess.PIPE, text=True)
    if "Duration" in process.stderr:
        print("✅ BAŞARILI! FFmpeg linki okuyabiliyor.")
        print("Gelen veri bilgisi:")
        for line in process.stderr.split('\n'):
            if "Stream #" in line:
                print(line)
    else:
        print("❌ HATA! FFmpeg linke bağlanamadı.")
        print("Hata sebebi şunlar olabilir: Link ölü, Token süresi dolmuş veya IP banlanmış.")
        print("\nFFmpeg Çıktısı:\n", process.stderr)
except FileNotFoundError:
    print("❌ HATA: FFmpeg yüklü değil! 'pkg install ffmpeg' yaz.")
