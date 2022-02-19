from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth   

es_host = 'bioghost2.usc.edu'
port = '9200'

es = Elasticsearch(
    [es_host],
    port=int(port),
    timeout=40
)
SITE_NAME = 'http://' + es_host + ':' + port + '/'
