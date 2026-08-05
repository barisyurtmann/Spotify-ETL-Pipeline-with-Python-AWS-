import requests
import base64

# Daha önce yazdığımız modülleri içeri aktarıyoruz
from src.pipeline.config import SpotifyConfig
from src.pipeline.utils.logger import get_logger

# Bu dosya için logger kanalımızı oluşturuyoruz
logger = get_logger(__name__)

class SpotifyClient:
    """Spotify API ile iletişimi yönetecek profesyonel istemci sınıfı."""
    
    def __init__(self, config: SpotifyConfig):
        # Sınıf başlatıldığında config objesini alır ve kaydeder
        self.config = config
        self.access_token = None
        self.base_url = "https://api.spotify.com/v1" # Spotify'ın ana adresi

    def authenticate(self) -> None:
        """Client Credentials yöntemi ile Spotify'dan token alır."""
        logger.info("Spotify API kimlik doğrulaması başlatılıyor...")
        
        # Senin bulduğun kod: Şifreleri Base64 formatına çevirme
        auth_string = f"{self.config.client_id}:{self.config.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        # Profesyonel Dokunuş: Hata yönetimi (Try-Except)
        try:
            # timeout=10 eklemek endüstri standardıdır (sonsuza kadar beklemesini önler)
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            # Eğer Spotify sunucusu 400 veya 500'lü bir hata dönerse, kodu burada patlatır ve except'e atar
            response.raise_for_status() 
            
            # Senin bulduğun kod: Token'ı alıp değişkene kaydetme
            self.access_token = response.json()["access_token"]
            
            # print() yerine logger kullanıyoruz ki JSON olarak buluta gitsin!
            logger.info("Spotify API token'ı başarıyla alındı.")
            
        except requests.exceptions.RequestException as e:
            # İnternet kopsa veya şifre yanlış olsa bile sistem sessizce ölmez, bize JSON log bırakır
            logger.error(f"Kimlik doğrulama başarısız oldu: {e}")
            raise # Hatayı yukarı fırlatarak pipeline'ın hatalı verilerle devam etmesini engelleriz


    def get_artist_top_tracks(self, artist_id: str, market: str = "US") -> list:
            """Belirtilen sanatçının en popüler parçalarını Spotify API'den çeker."""
            
            # 1. Geliştirme: Token var mı kontrolü
            if not self.access_token:
                logger.error("Token bulunamadı! İşlemden önce authenticate() çağrılmalı.")
                raise ValueError("Access token eksik.")

            # URL'yi manuel yazmak yerine base_url'den türetiyoruz
            endpoint = f"{self.base_url}/artists/{artist_id}/top-tracks"
            headers = {"Authorization": f"Bearer {self.access_token}","User-Agent": "SpotifyETLPipeline/1.0"}
            

            logger.info(f"Sanatçı ID ({artist_id}) için popüler şarkılar çekiliyor...")

            try:
                # 3. Geliştirme: params ve timeout eklendi
                response = requests.get(endpoint, headers=headers, timeout=10)
                response.raise_for_status()
                
                # API'den gelen JSON verisinden sadece 'tracks' listesini alıyoruz
                tracks = response.json().get("tracks", [])
                logger.info(f"Başarıyla {len(tracks)} adet şarkı çekildi.")
                
                # 4. Geliştirme: Ekrana yazdırmak (print) yerine veriyi döndürüyoruz
                return tracks

            except requests.exceptions.RequestException as e:

                if e.response is not None:
                    logger.error(f"Spotify API Detaylı Hata Mesajı: {e.response.text}")
                logger.error(f"Veri çekilirken API hatası oluştu: {e}")
                raise


    