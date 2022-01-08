from datetime import datetime
import logging
from flask import Flask, Response, app, request
from entites.BaseEntity import BaseApiResponse
from validation.http_api_validation import isValidationError, validateIsNumber, validationErrMessage
from usecases.CovidUseCase import CovidUseCase
import gladiator as gl


class CovidApiHandler():
    def __init__(self, flaskApp: Flask, covidUseCase: CovidUseCase):
        self.http = flaskApp
        self.useCase = covidUseCase # init usecase deps
        self.logger = logging.getLogger('root') # get root logger

    def getGeneralInformation(self):
        """handle request general information

        Returns:
            [json]: [response json]
        """
        # process use case
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
        """handle request get data yearly

        Returns:
            [json]: [response json]
        """
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

        # process use case
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

    def getDataByYear(self, year):
        """handle request get data by year

        Returns:
            [json]: [response json]
        """
        # validate request
        valErr = [validateIsNumber(year, "year")]


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

        # process use case
        result, err = self.useCase.getCaseByYear(year)
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
        # if data not found return epmty object
        if result == None:
            return Response(
                BaseApiResponse(
                    ok=False,
                    data={},
                    message='data not found'
                ).to_json(),
                status=404,
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

        @self.http.route('/yearly/<year>')
        def _getDataByYear(year):
            return self.getDataByYear(year)



