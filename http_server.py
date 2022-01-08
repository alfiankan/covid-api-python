import sqlite3
from flask import Flask
from sys import stdout

from handlers.CovidApiHandler import CovidApiHandler
from repositories.CovidDataRepository import CovidDataRepository
from usecases.CovidUseCase import CovidUseCase
import logging

def startServer():
    # HTTP API SERVER ENTRY POINT
    app = Flask(__name__)
    # set slash not strict
    app.url_map.strict_slashes = False

    # stream log to stdout for docker log
    stdoutHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
    stdoutHandler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logging.getLogger('root').addHandler(stdoutHandler)

    # starting dependeny injection
    db = sqlite3.connect('covid_database.db', isolation_level=None, check_same_thread=False)
    covidRepository = CovidDataRepository(db)
    covidApiUseCase = CovidUseCase(covidRepository)
    covidApiHandler = CovidApiHandler(app, covidApiUseCase)
    covidApiHandler.route()

    return app

if __name__ == "__main__":
    app = startServer()
    app.run(port=3000)


