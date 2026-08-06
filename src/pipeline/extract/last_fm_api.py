import requests

from src.pipeline.utils.logger import get_logger
from src.pipeline.config import SpotifyConfig
from dataclasses import dataclass

# Bu dosya için logger kanalımızı oluşturuyoruz
logger = get_logger(__name__)

@dataclass
class Last_fm_Client:
    config = SpotifyConfig()
    base_url = "http://ws.audioscrobbler.com/2.0/"

    params={
        'method':'chart.gettopartists',
        'api_key': config.client_id
    }

    
    
    response=requests.get(base_url,params=params)
    data=response.json()

    



