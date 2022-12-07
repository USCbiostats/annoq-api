from elasticsearch import Elasticsearch

es_host = 'http://bioghost2.usc.edu:9200'

es = Elasticsearch(es_host, timeout=40)
SITE_NAME = es_host  + '/'
