import asyncio
from pytgcalls.types import MediaStream, VideoQuality

async def start_restart_loop(chat_id: int, m3u8_url: str, stream_bridge):
    bekleme_suresi = 80 * 60 
    
    while True:
        await asyncio.sleep(bekleme_suresi)
        
        if chat_id not in stream_bridge.active_streams:
            print(f"⏹️ {chat_id} için yenileme döngüsü durduruldu.")
            break
            
        print(f"🔄 Siyah ekran koruması devrede! {chat_id} yayını yenileniyor...")
        
        try:
            await stream_bridge.call.leave_call(chat_id)
            await asyncio.sleep(2)
            
            # 🔥 AYAR: Burada da FHD_1080p yaptık
            stream_settings = MediaStream(
                m3u8_url,
                video_parameters=VideoQuality.FHD_1080p
            )
            await stream_bridge.call.play(chat_id, stream_settings)
            
            print(f"✅ {chat_id} yayını başarıyla tazelendi.")
            
        except Exception as e:
            print(f"❌ Yayın tazelenirken hata: {e}")
            break
