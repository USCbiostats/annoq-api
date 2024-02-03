import load_env
import logging
from flask import Flask,request,Response,jsonify, send_from_directory, abort
from flask_cors import CORS
from src.config.es import es
from src.gene_pos import map_gene, get_pos_from_gene_id, chromosomal_location_dic
from src.download import query_vcf, query_to_file
import uuid
import requests
import json
from src.config.settings import settings


app = Flask(__name__)
CORS(app)

werkzeug_logger = logging.getLogger('werkzeug')
file_handler = logging.FileHandler('access.log')
file_handler.setLevel(logging.INFO) 
werkzeug_logger.addHandler(file_handler)

# Setup logger for your Flask app
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/anno_tree')
def get_anno_tree():

    with open('data/anno_tree.json') as f:
        return  { 'result': json.load(f)}


@app.route('/gene')
def search_gene_pos():
    gene_name = request.args.get('gene')
    gene_id = map_gene(gene_name)
    gene_pos = get_pos_from_gene_id(gene_id, chromosomal_location_dic)
    gene_info = {'gene_id':gene_id, 'contig': '', 'start':0, 'end':0}
    if gene_pos:
        gene_info['contig'] = gene_pos[0]
        gene_info['start'] = gene_pos[1]
        gene_info['end'] = gene_pos[2]
    return jsonify({'gene_info':gene_info})


@app.route('/download/<folder>/<name>', methods=['GET'])
def download_file(folder, name):
    if not folder in settings.DOWNLOAD_DIR: 
        abort(400)
    return send_from_directory(folder, name, as_attachment=True)

@app.route('/total_res', methods=['GET','POST'])
def get_download_url():
    body = request.json
    query = {"query": body.get('query')}
    if body.get('_source'):
        query['_source'] = body['_source']
    filename = str(uuid.uuid4()) + '.txt'
    f = open(settings.DOWNLOAD_DIR + '/' + filename, 'w')
    query_to_file(es, query, f.write, f.write)
    return jsonify({"url": "/download/" + 'tmp/' + filename})

@app.route('/<idx>/ids', methods=['POST'])
def mget(idx):
    body = request.json
    ids = body.get('ids')
    source = body.get('_source')
    filename = str(uuid.uuid4()) + '.txt'
    f = open(settings.DOWNLOAD_DIR + '/' + filename, 'w')
    if (not ids) or (not source):
        abort(404)
    hits = {"hits":query_vcf(es, {"ids":ids, "_source":source}, f.write)}
    #query to file and return first page
    return jsonify({"hits":hits, "url": "/download/" + 'tmp/' + filename})

@app.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global SITE_NAME
    #print(request.get_json())
    if request.method=='GET':
        resp = requests.get(f'{settings.ES_SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = requests.post(f'{settings.ES_SITE_NAME}{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

if __name__ == '__main__':
    
    print(settings.API_URL, settings.API_PORT)
    app.run(host = settings.API_URL,port=settings.API_PORT, debug = settings.DEBUG)

