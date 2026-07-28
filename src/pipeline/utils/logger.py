import logging #Python'un içine yerleşik olarak gelen, sistemdeki olayları (hatalar, bilgi mesajları vb.) kayıt altına almak için kullanılan ana kütüphanedir. print()'in çok daha akıllı ve yetenekli abisi olarak düşünebilirsin.
import sys #Python'un üzerinde çalıştığı işletim sistemi (Windows, Linux vb.) ile iletişim kurmasını sağlayan modüldür. Biz bunu loglarımızı doğrudan terminal ekranına (sistemin standart çıktısına) fırlatmak için kullanıyoruz.
import os

# (Bu, JSON loglama için tüm dünyada en çok kullanılan standart Python kütüphanesidir.)
from pythonjsonlogger.json import JsonFormatter

def get_logger(name: str) -> logging.Logger: 
    """
    Belirtilen isimle (genellikle __name__) yapılandırılmış bir logger döndürür.

    Terminale insan okunabilir (metin), 'logs/' klasörüne ise 
    makine okunabilir (JSON) formatta çift kanallı loglama yapar.
    """
    logger = logging.getLogger(name) #İşin kalbi burasıdır. Python'a "Bana 'name' adında bir log kanalı aç veya daha önce açılmışsa onu getir" diyoruz. Her dosya (modül) kendi adıyla bir kanal açar. Böylece bir hata olduğunda hatanın config.py kanalından mı yoksa spotify_api.py kanalından mı geldiğini anında görebiliriz.
    
    # Logger'ın seviyesini belirliyoruz (INFO ve üzerindeki hataları gösterir)
    logger.setLevel(logging.INFO)#Logların bir önem sırası vardır (DEBUG, INFO, WARNING, ERROR, CRITICAL). Buraya INFO yazarak şifreyi belirliyoruz: "Bana sadece INFO (bilgilendirme) ve ondan daha ciddi olan (WARNING, ERROR) mesajları göster; önemsiz DEBUG detaylarıyla ekranı kirletme."


    # --- 1. KANAL: TERMİNAL (İnsanlar İçin Düz Metin) ---

    # Handler'ların birden fazla kez eklenmesini önlemek için kontrol, "Eğer bu logger'a daha önce bir ayar (handler) eklenmemişse ekle, eklenmişse dokunma"
    if not logger.handlers:
        # Log mesajımızın formatı: [Tarih/Saat] - [Dosya Adı] - [Seviye] - [Mesaj]
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Logları terminal (konsol) ekranına basmak için ayar
        console_handler = logging.StreamHandler(sys.stdout)#Handler (İşleyici), log mesajını alıp bir yere teslim eden kuryedir. StreamHandler ve sys.stdout kullanarak kuryeye "Bu mesajları al ve kullanıcının terminal ekranına yazdır" talimatını veriyoruz. İleride bunu FileHandler yaparak logları bir .txt dosyasına da kaydedebiliriz.
        console_handler.setFormatter(formatter)
        
        # Handler'ı logger'a ekle
        logger.addHandler(console_handler)


    # --- 2. KANAL: DOSYA (Sistemler/Bulut İçin JSON) ---

    # Ana dizinde 'logs' klasörü yoksa otomatik oluşturur
        os.makedirs("logs", exist_ok=True)
        
        file_handler = logging.FileHandler("logs/pipeline.log", encoding="utf-8")
        
        # JSON formatında hangi bilgilerin olacağını belirliyoruz
        json_formatter = JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            json_ensure_ascii=False # <-- TÜRKÇE KARAKTER DESTEĞİ İÇİN BU SATIRI EKLEDİK
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
    
        
    return logger