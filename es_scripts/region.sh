. host.sh

curl -XPOST "$host/annoq-annotations-v2/_search?pretty" \
-H 'Content-Type: application/json' \
-d '{
"query": { 
    "bool": {
	"filter": [
		{"term": {"chr":"2"}},
		{"range" : { "pos" : { "gte" : 10, "lte" : 20000 } }}]
}}}'
