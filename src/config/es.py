from elasticsearch import Elasticsearch
from src.config.settings import settings

es = Elasticsearch(settings.ANNOQ_ES_URL, timeout= settings.ANNOQ_ES_TIMEOUT)
