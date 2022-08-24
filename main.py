from flask import Flask
from waitress import serve
from Assets import *
import socket, os

HOST = '0.0.0.0'
PORT = 80
THREADS = 6

UPLOAD_FOLDER = 'data'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

main = MainWebsite(app)

if __name__ == '__main__':
    print(f"connecting with ip: {IP} and port: {PORT}")
    serve(app, host=HOST, port=PORT, threads=THREADS)