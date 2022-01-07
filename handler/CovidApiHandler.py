from datetime import datetime
import logging
from flask import Flask, Response, app, request
from entity.BaseEntity import BaseApiResponse
from handler.HandlerValidation import isValidationError, validateIsEmptyQueryParam, validateIsNumber, validateIsTypeValid, validationErrMessage
from usecase.CovidUseCase import CovidUseCase
import time
import gladiator as gl


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
            return Response(
                BaseApiResponse(
                    ok=False,
                    data={},
                    message='something wrong with server'
                ).to_json(),
                status=500,
                content_type='application/json'
            )

        return Response(
            BaseApiResponse(
                ok=True,
                data=result,
                message='success'
            ).to_json(),
            status=200,
            content_type='application/json'
        )

    def getYearlyData(self):
        # get query param since, upto
        since = request.args.get('since', 2020)
        upto = request.args.get('upto', datetime.now().year)

        # validate request
        valErr = [
            validateIsNumber(since, "since"),
            validateIsNumber(upto, "upto")
        ]


        if isValidationError(valErr):
            return Response(
                BaseApiResponse(
                    ok=False,
                    data={},
                    message='Validation error, {}'.format(validationErrMessage(valErr))
                ).to_json(),
                status=422,
                content_type='application/json'
            )


        result, err = self.useCase.getYearlyCasesList(int(since), int(upto))

        if err != None:
            self.logger.error(err)
            return Response(
                BaseApiResponse(
                    ok=False,
                    data={},
                    message='something wrong with server'
                ).to_json(),
                status=500,
                content_type='application/json'
            )
        return Response(
            BaseApiResponse(
                ok=True,
                data=result,
                message='success'
            ).to_json(),
            status=200,
            content_type='application/json'
        )

    def route(self):
        @self.http.route('/', methods=['GET'])
        def _getGeneralInformation():
            return self.getGeneralInformation()

        @self.http.route('/yearly', methods=['GET'])
        def _getYearlyData():
            return self.getYearlyData()




