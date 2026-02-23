from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

class StreamBridge:
    def __init__(self, app):
        self.app = app
        self.call = PyTgCalls(self.app)
        self.active_streams = {} 
        self.restart_tasks = {}

    async def start_bridge(self):
        # Bu komut Userbot'u da otomatik başlatır
        await self.call.start()
        print("✅ Gelişmiş Yayın Motoru (v2) Başlatıldı")

    async def play(self, chat_id: int, m3u8_url: str):
        try:
            # 1. Eski yayın varsa temizle (Çakışmayı önler)
            try:
                await self.call.leave_call(chat_id)
            except:
                pass

            # 2. Senin istediğin o Profesyonel FFmpeg Ayarları
            # PyTgCalls v2'de bu ayarlar 'ffmpeg_parameters' içine eklenir.
            # Buraya hem User-Agent (Siyah ekran çözümü) hem Reconnect (Donma çözümü) ekledik.
            ozel_ffmpeg_ayarlari = (
                "-headers 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' "
                "-reconnect 1 "                 # İnternet giderse tekrar bağlan
                "-reconnect_streamed 1 "        # Akış koparsa tekrar yakala
                "-reconnect_delay_max 5 "       # En fazla 5 saniye bekle
                "-allowed_extensions ALL "      # Tüm uzantılara izin ver
                "-protocol_whitelist file,http,https,tcp,tls,crypto " # Tüm protokolleri aç
                "-analyzeduration 15000000 "    # Analiz süresini artır (Yayını daha hızlı açar)
                "-probesize 15000000"           # Ön bellek boyutunu artır
            )

            # 3. Akışı Hazırla
            stream = MediaStream(
                m3u8_url,
                # Görüntü kalitesini kütüphanenin otomatik ayarlamasına izin veriyoruz (En stabil yöntem)
                # Senin yazdığın bitrate ayarlarını kütüphane bu modda kendi halleder.
                video_parameters=VideoQuality.HD_720p, 
                audio_parameters=AudioQuality.STUDIO,
                ffmpeg_parameters=ozel_ffmpeg_ayarlari # İşte sihirli ayarlar burada!
            )

            # 4. Yayını Başlat (Eski sürümdeki join_group_call yerine play kullanıyoruz)
            await self.call.play(chat_id, stream)

            self.active_streams[chat_id] = m3u8_url
            print(f"🔥 Yayın Başladı: {chat_id}")
            return True

        except Exception as e:
            print(f"❌ Yayın başlatılamadı ({chat_id}): {e}")
            return False

    async def stop(self, chat_id: int):
        try:
            await self.call.leave_call(chat_id)
            if chat_id in self.active_streams:
                del self.active_streams[chat_id]
            if chat_id in self.restart_tasks:
                self.restart_tasks[chat_id].cancel()
                del self.restart_tasks[chat_id]
            print(f"🛑 Yayın Durduruldu: {chat_id}")
            return True
        except Exception as e:
            print(f"❌ Durdurma hatası ({chat_id}): {e}")
            return False
