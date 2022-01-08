from datetime import datetime
import logging
from math import sin
from flask import Flask, Response, app, request
from entites.BaseEntity import BaseApiResponse
from validation.http_api_validation import isValidationError, validateIsNumber, validateIsmatchDateFormat, validationErrMessage
from usecases.CovidUseCase import CovidUseCase
import gladiator as gl
import time

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
            return json yearly data if empty query param return all yearly data
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

    def getMonthlyData(self):
        """handle request get data monthly
            return json monthly data if empty query param return all monthly data

        Returns:
            [json]: [response json]
        """
        # get query param since, upto
        since = request.args.get('since', '2020.01')
        upto = request.args.get('upto', datetime.utcfromtimestamp(time.time()).strftime("%Y.%m"))

        # validate request
        valErr = [
            validateIsmatchDateFormat(since, '%Y.%m', 'since', '<year>.<month> eg. 2020.01'),
            validateIsmatchDateFormat(upto, '%Y.%m', 'upto', '<year>.<month> eg. 2020.01')
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
        result, err = self.useCase.getMonthlyCase(since, upto)

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

    def getMonthlyDataByYear(self, year):
        """handle request get data monthly in a year
            returning json data per month in spesific year
            return all month in year if query param empty

        Returns:
            [json]: [response json]
        """
        since = request.args.get('since', '{}.01'.format(year))
        upto = request.args.get('upto', '{}.12'.format(year))
        # validate request query param
        valErr = [
            validateIsNumber(year, "year"),
            validateIsmatchDateFormat(since, '%Y.%m', 'since', '<year>.<month> eg. 2020.01'),
            validateIsmatchDateFormat(upto, '%Y.%m', 'upto', '<year>.<month> eg. 2020.01')
        ]

        # cek if month requested is in year param
        try:
            if datetime.strptime(since, "%Y.%m").timetuple().tm_year != int(year) or datetime.strptime(upto, "%Y.%m").timetuple().tm_year != int(year):
                valErr.append('month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)')
        except:
            pass

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
        result, err = self.useCase.getMonthlyCase(since, upto)

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

        @self.http.route('/yearly/<year>')
        def _getDataByYear(year):
            return self.getDataByYear(year)

        @self.http.route('/monthly', methods=['GET'])
        def _getMonthlyData():
            return self.getMonthlyData()

        @self.http.route('/monthly/<year>', methods=['GET'])
        def _getMonthlyDataByYear(year):
            return self.getMonthlyDataByYear(year)
