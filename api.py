import sqlite3
from flask import Flask
from sys import stdout
from handlers.CovidApiHandler import CovidApiHandler
from handlers.VaccinationApiHandler import VaccinationApiHandler
from repositories.CovidDataRepository import CovidDataRepository
from repositories.VaccinationDataRepository import VaccinationDataRepository
from usecases.CovidUseCase import CovidUseCase
from usecases.VaccinationUseCase import VaccinationUseCase
from repositories.CovidTestDataRepository import CovidTestDataRepository
from usecases.CovidTestUseCase import CovidTestUseCase
from handlers.CovidTestApiHandler import CovidTestApiHandler
import logging


# HTTP API SERVER ENTRY POINT
app = Flask(__name__)

# set slash not strict
app.url_map.strict_slashes = False

# stream log to stdout for log
logging.basicConfig(
    filename='logs/applog.log',
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
)

# starting dependeny injection
db = sqlite3.connect(
    'covid_database.db',
    isolation_level=None,
    check_same_thread=False
)

# create health check endpoint
@app.route('/health', methods=['GET'])
def healthCheck():
    return 'ok'

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


# covid test data
covidTestRepository = CovidTestDataRepository(db)
covidTestApiUseCase = CovidTestUseCase(covidTestRepository)
covidTestApiHandler = CovidTestApiHandler(app, covidTestApiUseCase)
covidTestApiHandler.route()


if __name__ == "__main__":
    app.run(port=3000)
