from flask import Flask, jsonify
from entity.BaseEntity import BaseApiResponse
from usecase.CovidUseCase import CovidUseCase
import time


class CovidApiHandler():
    def __init__(self, flaskApp: Flask, covidUseCase: CovidUseCase):
        self.http = flaskApp
        self.useCase = covidUseCase

    def getGeneralInformation(self):
        return BaseApiResponse(ok=True, data="Hello World", message="success").to_json()

    def route(self):
        @self.http.route("/", methods=["GET"])
        def _getGeneralInformation():
            return self.getGeneralInformation()




