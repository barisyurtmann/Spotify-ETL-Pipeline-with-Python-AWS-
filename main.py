import os
from dotenv import load_dotenv

# Kendi yazdığımız modülleri (departmanları) çağırıyoruz
from src.pipeline.config import SpotifyConfig
from src.pipeline.utils.logger import get_logger
from src.pipeline.extract.spotify_api import SpotifyClient
from src.pipeline.extract.last_fm_api import Last_fm_Client

def main():
    # 1. Şifreleri .env dosyasından sisteme yükle
    load_dotenv()
    
    # 2. Ana logger'ı başlat
    logger = get_logger(__name__)
    logger.info("Spotify ETL Pipeline başlatılıyor...")

    try:

        logger.info("Extract aşaması başlatılıyor...")
        client = Last_fm_Client
        

        # 6. Test verisi çek (Örnek: Coldplay'in en popüler şarkıları)
        top_tracks = client.get_playlist()

        logger.info(f"Pipeline başarıyla tamamlandı. {len(top_tracks)} şarkı çekildi.")

        

    except Exception as e:
        # Kodun herhangi bir yerinde hata çıkarsa, burada yakalanıp JSON olarak loglanacak
        logger.error(f"Pipeline çalışırken kritik bir hata oluştu: {e}")
        raise




    

if __name__ == "__main__":
    main()

