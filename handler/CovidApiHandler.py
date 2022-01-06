import logging
from flask import Flask, Response
from entity.BaseEntity import BaseApiResponse
from usecase.CovidUseCase import CovidUseCase
import time


class CovidApiHandler():
    def __init__(self, flaskApp: Flask, covidUseCase: CovidUseCase):
        self.http = flaskApp
        self.useCase = covidUseCase
        self.logger = logging.getLogger('root')

    def getGeneralInformation(self):
        result, err = self.useCase.getGeneralInformation()
        # TODO: handle loging
        if err != None:
            self.logger.error(err)
            return Response(BaseApiResponse(ok=False, data={}, message='something wrong with server').to_json(), status=500, content_type='application/json')
        return Response(BaseApiResponse(ok=True, data=result, message='success').to_json(), status=200, content_type='application/json')

    def route(self):
        @self.http.route('/', methods=['GET'])
        def _getGeneralInformation():
            return self.getGeneralInformation()




