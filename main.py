import os
from dotenv import load_dotenv

# Kendi yazdığımız modülleri (departmanları) çağırıyoruz
from src.pipeline.config import SpotifyConfig
from src.pipeline.utils.logger import get_logger
from src.pipeline.extract.spotify_api import SpotifyClient

def main():
    # 1. Şifreleri .env dosyasından sisteme yükle
    load_dotenv()
    
    # 2. Ana logger'ı başlat
    logger = get_logger(__name__)
    logger.info("Spotify ETL Pipeline başlatılıyor...")

    try:
        # 3. Config (Ayarlar) Objesini Oluştur
        # (Şifreleri çevresel değişkenlerden çekiyoruz ki koda yazılı kalmasın)
        config = SpotifyConfig()

        # 4. Extract (Çıkarma) Katmanını Başlat
        logger.info("Extract aşaması başlatılıyor...")
        client = SpotifyClient(config)
        
        # 5. Spotify'a giriş yap (Token al)
        client.authenticate()
    
        # 6. Test verisi çek (Örnek: Coldplay'in en popüler şarkıları)
        playlist_id = "6ReOmXz6Yd3u1JvjcqjbFW" 
        top_tracks = client.get_playlist_top_tracks(playlist_id=playlist_id)

        logger.info(f"Pipeline başarıyla tamamlandı. {len(top_tracks)} şarkı çekildi.")

        

    except Exception as e:
        # Kodun herhangi bir yerinde hata çıkarsa, burada yakalanıp JSON olarak loglanacak
        logger.error(f"Pipeline çalışırken kritik bir hata oluştu: {e}")
        raise




    

if __name__ == "__main__":
    main()

