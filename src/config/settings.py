import os
from pydantic import BaseSettings

class Settings(BaseSettings):
        
    DEBUG:bool=os.environ.get('DEBUG')
    API_URL:str=os.environ.get('API_URL')
    API_PORT:int=os.environ.get('API_PORT')
    ANNOQ_ES_URL:str=os.environ.get('ANNOQ_ES_URL')
    ANNOQ_ES_PORT:int=os.environ.get('ANNOQ_ES_PORT')
    ANNOQ_ES_TIMEOUT:int=os.environ.get('ANNOQ_ES_TIMEOUT')
    ANNOQ_ANNOTATIONS_INDEX:str=os.environ.get('ANNOQ_ANNOTATIONS_INDEX')
    DOWNLOAD_DIR :str= os.environ.get('DOWNLOAD_DIR')
    DOWNLOAD_SIZE :int=os.environ.get('DOWNLOAD_SIZE')
    
    ES_SITE_NAME= f'{ANNOQ_ES_URL}/'




settings = Settings()