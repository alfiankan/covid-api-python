from api import startApi
from flask.app import Flask

if __name__ == '__main__':
    app: Flask = startApi()
    app.run(debug=False)
