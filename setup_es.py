from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth   

es_host = 'http://bioghost2.usc.edu'
port = '9200'

es = Elasticsearch(
    [es_host],
    port=int(port),
    timeout=40
)
SITE_NAME = 'https://' + es_host + ':' + port + '/'
