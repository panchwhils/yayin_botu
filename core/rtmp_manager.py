import subprocess
import asyncio
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

# AYARLAR
RESTART_INTERVAL = 80 * 60  # 80 Dakika (Saniye cinsinden)

class RTMPStreamer:
    def __init__(self, name, m3u8_url, rtmp_url):
        self.name = name
        self.m3u8_url = m3u8_url
        self.rtmp_url = rtmp_url
        self.process = None

    async def start_stream(self):
        # Telegram için optimize edilmiş FFmpeg parametreleri
        ffmpeg_cmd = [
            'ffmpeg',
            '-re',
            '-headers', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-i', self.m3u8_url,
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-b:v', '3500k', # 1080p Bitrate
            '-maxrate', '3500k',
            '-bufsize', '7000k',
            '-pix_fmt', 'yuv420p',
            '-g', '60',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-f', 'flv',
            self.rtmp_url
        ]

        print(f"🚀 [{self.name}] Yayın başlatılıyor...")
        self.process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def stop_stream(self):
        if self.process:
            print(f"♻️ [{self.name}] Restart için yayın durduruluyor...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

async def run_with_restart(streamer):
    while True:
        await streamer.start_stream()
        print(f"⏰ [{streamer.name}] 80 dakikalık sayaç başladı.")
        
        # 80 dakika bekle
        await asyncio.sleep(RESTART_INTERVAL)
        
        print(f"🔄 [{streamer.name}] 80 dakika doldu, restart atılıyor...")
        streamer.stop_stream()
        await asyncio.sleep(5) # Temiz bir başlangıç için kısa bekleme

async def main():
    # JSON Dosyasını Oku
    try:
        with open("channels.json", "r") as f:
            channels = json.load(f)
    except Exception as e:
        print(f"❌ JSON okuma hatası: {e}")
        return

    tasks = []
    for name, data in channels.items():
        # RTMP URL ve Stream Key'i channels.json içinde sakladığını varsayıyorum
        # JSON yapın: {"Kanal1": {"m3u8_url": "...", "rtmp_url": "rtmps://..."}}
        streamer = RTMPStreamer(name, data['m3u8_url'], data['rtmp_url'])
        tasks.append(run_with_restart(streamer))

    if tasks:
        print(f"✅ {len(tasks)} adet yayın için sistem hazır.")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tüm yayınlar durduruldu.")
