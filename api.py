import sqlite3
from flask import Flask
from sys import stdout

from handlers.CovidApiHandler import CovidApiHandler
from handlers.VaccinationApiHandler import VaccinationApiHandler
from repositories.CovidDataRepository import CovidDataRepository
from repositories.VaccinationDataRepository import VaccinationDataRepository
from usecases.CovidUseCase import CovidUseCase
from usecases.VaccinationUseCase import VaccinationUseCase
import logging


def startApi():
    # HTTP API SERVER ENTRY POINT
    app = Flask(__name__)
    # set slash not strict
    app.url_map.strict_slashes = False

    # stream log to stdout for docker log
    stdoutHandler = logging.StreamHandler(stdout)
    stdoutHandler.setFormatter(
        logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    )
    logging.getLogger('root').addHandler(stdoutHandler)

    # starting dependeny injection
    db = sqlite3.connect(
        'covid_database.db',
        isolation_level=None,
        check_same_thread=False
    )

    # covid case
    covidRepository = CovidDataRepository(db)
    covidApiUseCase = CovidUseCase(covidRepository)
    covidApiHandler = CovidApiHandler(app, covidApiUseCase)
    covidApiHandler.route()

    # vaccination data
    vaccRepository = VaccinationDataRepository(db)
    vaccApiUseCase = VaccinationUseCase(vaccRepository)
    vaccApiHandler = VaccinationApiHandler(app, vaccApiUseCase)
    vaccApiHandler.route()

    return app


if __name__ == "__main__":
    app = startApi()
    app.run(port=3000)
