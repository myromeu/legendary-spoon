from flask import Flask, Response, request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import shell_scripts

app = Flask(__name__)
api_path = '/api/v1'

@app.route('/')
def index():
    host = request.host
    return Response('Try <a href="/api/v1/get_mongo">{0}/api/v1/get_mongo</a> or <a href="/api/v1/get_rabbit">{0}/api/v1/get_rabbit</a>'.format(host))

@app.route(api_path + '/get_rabbit', methods=['GET'])
def get_rabbit():
    return Response(shell_scripts.RABBIT_SCRIPT, mimetype='text/plain')

@app.route(api_path + '/get_mongo', methods=['GET'])
def get_mongo():
    return Response(shell_scripts.MONGO_SCRIPT, mimetype='text/plain')

@app.route(api_path + '/test_mongo', methods=['GET'])
def test_mongo():
    host, port = request.args.get('host', default='localhost'), request.args.get('port', default='27017')
    uri = "mongodb://%s:%s/admin" % (host, port)
    client = MongoClient(uri, maxPoolSize=1, connectTimeoutMS=3000, serverSelectionTimeoutMS=3000)
    resp = Response('false', mimetype='text/plain')
    try:
        if client.admin.command('ismaster')['ok'] == 1:
            resp = Response('true', mimetype='text/plain')
    except ConnectionFailure:
        resp = Response('false', mimetype='text/plain')

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
