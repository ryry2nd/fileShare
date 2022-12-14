from flask import Flask
from waitress import serve
from Assets import *
import socket, os

HOST = '0.0.0.0'
PORT = 80
THREADS = 6

SECRET_KEY = os.urandom(24)

with open("dataPath.txt") as file:
    UPLOAD_FOLDER = file.read().strip()

if not os.path.exists("password.txt"):
    open("password.txt", "x").close()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

with open("password.txt") as file:
    PASSWORD = file.read().strip()

app = Flask(__name__)

app.config['password'] = PASSWORD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

main = MainWebsite(app)

if __name__ == '__main__':
    print(f"connecting with ip: {IP} and port: {PORT}")
    #app.run(host=HOST, port=PORT)
    serve(app, host=HOST, port=PORT, threads=THREADS)