import os
from flask import Flask
from sys import stdout

from handler.CovidApiHandler import CovidApiHandler
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase
import logging



if __name__ == "__main__":
    app = Flask(__name__)

    # save log to file on production
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    # stream log to stdout for docker log
    stdoutHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
    stdoutHandler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logging.getLogger('root').addHandler(stdoutHandler)

    # starting dependeny injection
    covidRepository = CovidDataRepository()
    covidApiUseCase = CovidUseCase(covidRepository)
    covidApiHandler = CovidApiHandler(app, covidApiUseCase)
    covidApiHandler.route()


    app.run('localhost', 3000, debug=False)

