import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass # init yazmamıza gerek kalmadan class oluşturmak için dataclass kullanıyoruz. böylece init kısmını atlayıp direk postinit ile olmuşmu kontrol ediyoruz.

# Oluşturduğumuz özel logger fonksiyonunu projemize dahil ediyoruz
from src.pipeline.utils.logger import get_logger

# Bu dosya çalıştığında __name__ otomatik olarak "src.pipeline.config" değerini alır
# Böylece log mesajında "Bu mesaj config.py içinden geldi" bilgisini görebiliriz
logger = get_logger(__name__)

# 1. Aşama: .env dosyası pathi bulma
env_yolu = find_dotenv()
logger.info(f"Bulunan .env dosyasının konumu: '{env_yolu}'")

# 2. Aşama: .env Dosyayı yükleme(.env dosyasındaki şifreleri Python ortamına yükler)
load_dotenv(env_yolu)


print("-" * 40)

@dataclass
class SpotifyConfig:
    client_id: str = os.getenv("SPOTIFY_CLIENT_ID","")
    client_secret: str = os.getenv("SPOTIFY_CLIENT_SECRET","")#("SPOTIFY_CLIENT_SECRET","") virgülden sonra "" koymamızın sebebi str istiyor olmamız. olurda none gelirse boş olarak döndür demek.

    # Şifrelerden biri eksikse program daha en başında hata fırlatır
    def __post_init__(self):
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify kimlik bilgileri eksik! Lütfen .env dosyasını kontrol et.")

# Tüm projede import edip kullanacağımız tekil obje
#config = SpotifyConfig()
#logger.info("SpotifyConfig objesi sorunsuz bir şekilde oluşturuldu ve doğrulandı.")