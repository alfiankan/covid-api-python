from http_server import startServer
from flask.app import Flask

if __name__ == '__main__':
    app: Flask = startServer()
    app.run(debug=False)
