from flask import Flask, Response, request
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

if __name__ == '__main__':
    app.run()
