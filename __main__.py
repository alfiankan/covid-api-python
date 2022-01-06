from flask import Flask

from handler.CovidApiHandler import CovidApiHandler
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase


if __name__ == "__main__":
    app = Flask(__name__)

    # starting dependeny injection
    covidRepository = CovidDataRepository()
    covidApiUseCase = CovidUseCase(covidRepository)
    covidApiHandler = CovidApiHandler(app, covidApiUseCase)
    covidApiHandler.route()

    app.run("localhost", 3000, debug=False)
