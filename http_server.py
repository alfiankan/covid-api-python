import sqlite3
from flask import Flask
from sys import stdout

from handler.CovidApiHandler import CovidApiHandler
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase
import logging

# HTTP API SERVER ENTRY POINT
app = Flask(__name__)

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



