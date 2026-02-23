import os
import signal
import subprocess
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

bot = Client(
    "yayin_botu",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")  # Mevcut sistem çalışır
)


class RTMPManager:
    def __init__(self):
        self.process = None
        self.stream_key = "3148286961:alfharKB3EgoTmsv2QdV9w"
        self.rtmp_url = f"rtmps://dc4-1.rtmp.t.me/s/{self.stream_key}"

        self.headers = (
            "User-Agent: Mozilla/5.0\r\n"
            "Accept: */*\r\n"
            "Connection: keep-alive\r\n"
            "Referer: http://tr3.153689.xyz/\r\n"
        )

    async def start_stream(self, m3u8_url):
        await self.stop_stream()

        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-headers", self.headers,
            "-i", m3u8_url,

            # VIDEO (senin stabil ayarın)
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",
            "-profile:v", "baseline",
            "-level", "3.1",

            # AUDIO
            "-c:a", "aac",
            "-ar", "44100",
            "-b:a", "128k",

            "-f", "flv",
            self.rtmp_url
        ]

        try:
            # 🔥 DETACHED MODE (nohup gibi)
            self.process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )

            print("🚀 Yayın Başlatıldı")
            return True

        except Exception as e:
            print("❌ FFmpeg Hatası:", e)
            return False

    async def stop_stream(self):
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except:
                pass
            self.process = None
            print("🛑 Yayın Durduruldu")


yayin_motoru = RTMPManager()


if __name__ == "__main__":
    print("⏳ RTMP TV Bot Başlatılıyor...")
    print("📡 RTMP:", yayin_motoru.rtmp_url)
    print("✅ Bot Aktif!")
    bot.run()
