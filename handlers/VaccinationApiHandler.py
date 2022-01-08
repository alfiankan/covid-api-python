from datetime import datetime
from calendar import monthrange
import logging
from flask import Flask, Response, request
from entites.BaseEntity import BaseApiResponse
from validation.http_api_validation import isValidationError, validateIsNumber, validateIsmatchDateFormat, validationErrMessage
from usecases.VaccinationUseCase import VaccinationUseCase
import time


class VaccinationApiHandler():
    def __init__(self, flaskApp: Flask, vaccUseCase: VaccinationUseCase):
        self.http = flaskApp
        # init usecase deps
        self.useCase = vaccUseCase
        # get root logger
        self.logger = logging.getLogger('root')

    def serverErrorResponse(self):
        """
        Returns:
            return api response serverity error
        """
        return Response(
            BaseApiResponse(ok=False, data={}, message='something wrong with server').to_json(),
            status=500,
            content_type='application/json'
        )

    def notFoundResponse(self):
        """
        Returns:
            return api response serverity error
        """
        return Response(
            BaseApiResponse(ok=False, data={}, message='data not found').to_json(),
            status=404,
            content_type='application/json'
        )

    def getGeneralInformation(self):
        """handle request general information

        Returns:
            [json]: [response json]
        """

        # process use case
        result, err = self.useCase.getGeneralInformation()
        # TODO: handle loging
        if err is not None:
            self.logger.error(err)
            # return server error json
            return self.serverErrorResponse()

        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
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
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getYearlyDatasList(int(since), int(upto))
        if err is not None:
            self.logger.error(err)
            # return server error json
            return self.serverErrorResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
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
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getDataByYear(year)
        if err is not None:
            self.logger.error(err)
            # return server error json
            return self.serverErrorResponse()

        # if data not found return epmty object
        if result is None:
            # return not found
            return self.notFoundResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
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
            validateIsmatchDateFormat(since, '%Y.%m', 'since', '<year>.<month> eg. 2020.01  and cant be empty'),
            validateIsmatchDateFormat(upto, '%Y.%m', 'upto', '<year>.<month> eg. 2020.01  and cant be empty')
        ]

        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getMonthlyData(since, upto)
        if err is not None:
            self.logger.error(err)
            # return not found
            return self.notFoundResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
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
            validateIsmatchDateFormat(since, '%Y.%m', 'since', '<year>.<month> eg. 2020.01  and cant be empty'),
            validateIsmatchDateFormat(upto, '%Y.%m', 'upto', '<year>.<month> eg. 2020.01  and cant be empty')
        ]

        # cek if month requested is in year param
        try:
            if datetime.strptime(since, "%Y.%m").timetuple().tm_year != int(year) or datetime.strptime(upto, "%Y.%m").timetuple().tm_year != int(year):
                valErr.append('month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)')
        except ValueError:
            pass
        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getMonthlyData(since, upto)
        if err is not None:
            self.logger.error(err)
            # return server error
            return self.serverErrorResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
            status=200,
            content_type='application/json'
        )

    def getMonthlyDataByYearMonth(self, year, month):
        """handle request get data monthly by year and month
            return single json monthly data

        Returns:
            [json]: [response json]
        """

        # validate request
        valErr = [
            validateIsmatchDateFormat(year, '%Y', 'since', '<year>.<month> eg. 2020  and cant be empty'),
            validateIsmatchDateFormat(month, '%m', 'upto', '<year>.<month> eg. 09  and cant be empty')
        ]
        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getMonthlyData('{}.{}'.format(year, month), '{}.{}'.format(year, month))
        if err is not None:
            self.logger.error(err)
            return Response(
                BaseApiResponse(ok=False, data={}, message='something wrong with server').to_json(),
                status=500,
                content_type='application/json'
            )

        if len(result) == 0:
            # return not found
            return self.notFoundResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result[0], message='success').to_json(),
            status=200,
            content_type='application/json'
        )

    def getDailyData(self):
        """handle request get data daily
            return json daily data if empty query param return all daily data

        Returns:
            [json]: [response json]
        """
        # get query param since, upto
        since = request.args.get('since', '2020.01.01')
        upto = request.args.get('upto', datetime.utcfromtimestamp(time.time()).strftime("%Y.%m.%d"))

        # validate request
        valErr = [
            validateIsmatchDateFormat(since, '%Y.%m.%d', 'since', '<year>.<month> eg. 2020.01.01 and cant be empty'),
            validateIsmatchDateFormat(upto, '%Y.%m.%d', 'upto', '<year>.<month> eg. 2020.01.01 and cant be empty')
        ]
        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getDailyData(since, upto)
        if err is not None:
            self.logger.error(err)
            return self.serverErrorResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
            status=200,
            content_type='application/json'
        )

    def getDailyDataByYear(self, year):
        """handle request get data daily in a year
            returning json data per day in spesific year
            return all day in year if query param empty

        Returns:
            [json]: [response json]
        """

        since = request.args.get('since', '{}.01.01'.format(year))
        upto = request.args.get('upto', '{}.12.31'.format(year))
        # validate request query param
        valErr = [
            validateIsNumber(year, 'year'),
            validateIsmatchDateFormat(since, '%Y.%m.%d', 'since', '<year>.<month> eg. 2020.01.01  and cant be empty'),
            validateIsmatchDateFormat(upto, '%Y.%m.%d', 'upto', '<year>.<month> eg. 2020.01.01  and cant be empty')
        ]
        # cek if day requested is in year param
        try:
            if datetime.strptime(since, "%Y.%m.%d").timetuple().tm_year != int(year) or datetime.strptime(upto, "%Y.%m.%d").timetuple().tm_year != int(year):
                valErr.append('date format request is not in year, make sure <year> in ?since=<year>.<month>.<day> and ?upto=<year>.<month>.<day> /daily/<year> is same year, (eg. daily/2021?since=2021.05.01&upto=2021.09.01)')
        except ValueError:
            pass
        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getDailyData(since, upto)
        if err is not None:
            self.logger.error(err)
            # retuen server error
            return self.serverErrorResponse()

        # return success response
        return Response(
                BaseApiResponse(ok=True, data=result, message='success').to_json(),
                status=200,
                content_type='application/json'
        )

    def getDailyDataInYearMonth(self, year, month):
        """handle request get data daily in year and month
            return single json daily data

        Returns:
            [json]: [response json]
        """
        # validate request query param
        valErr = [
            validateIsNumber(year, "year"),
            validateIsNumber(month, "month")
        ]
        # validation month year valid
        try:
            monthrange(int(year), int(month))[1]
        except ValueError:
            valErr.append('make sure year month and date in 2021.01.01 date format')
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )
        # calculate total day of month

        totalDayOfMonth = monthrange(int(year), int(month))[1]
        since = request.args.get('since', '{}.{}.01'.format(year, month))
        upto = request.args.get('upto', '{}.{}.{}'.format(year, month, totalDayOfMonth))

        # validate request query param
        valErr.append(validateIsmatchDateFormat(since, '%Y.%m.%d', 'since', '<year>.<month>.<date> eg. 2020.01.01  and cant be empty'))
        valErr.append(validateIsmatchDateFormat(upto, '%Y.%m.%d', 'upto', '<year>.<month>.<date> eg. 2020.01.01  and cant be empty'))

        # cek if month requested is in year param
        try:
            dateSince = datetime.strptime(since, "%Y.%m.%d").timetuple()
            dateUpto = datetime.strptime(upto, "%Y.%m.%d").timetuple()
            if dateSince.tm_year != int(year) or dateUpto.tm_year != int(year) or dateSince.tm_mon != int(month.strip("0")) or dateUpto.tm_mon != int(month.strip("0")):
                valErr.append('month format request is not in year, make sure <year> in ?since=<year>.<month>.<date> and ?upto=<year>.<month>.<date>  /daily/<year>/<month> is same year, (eg. daily/2021/05?since=2021.05.01&upto=2021.05.10)')
        except ValueError:
            pass

        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getDailyData(since, upto)
        if err is not None:
            self.logger.error(err)
            # return server error
            return self.serverErrorResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result, message='success').to_json(),
            status=200,
            content_type='application/json'
        )

    def getDailyDataByDate(self, year, month, date):
        """handle request get data monthly by year and month
            return single json monthly data

        Returns:
            [json]: [response json]
        """

        # validate request
        valErr = [
            validateIsmatchDateFormat(year, '%Y', 'year', '<year>.<month>.<date> eg. 2020  and cant be empty'),
            validateIsmatchDateFormat(month, '%m', 'month', '<year>.<month>.<date> eg. 09  and cant be empty'),
            validateIsmatchDateFormat(date, '%d', 'date', '<year>.<month>.<date> eg. 09  and cant be empty')
        ]

        if isValidationError(valErr):
            return Response(
                BaseApiResponse(ok=False, data={}, message='Validation error, {}'.format(validationErrMessage(valErr))).to_json(),
                status=422,
                content_type='application/json'
            )

        # process use case
        result, err = self.useCase.getDailyData('{}.{}.{}'.format(year, month, date), '{}.{}.{}'.format(year, month, date))

        if err is not None:
            self.logger.error(err)
            # return server error
            return self.serverErrorResponse()

        if len(result) == 0:
            # return not found
            return self.notFoundResponse()

        # return success response
        return Response(
            BaseApiResponse(ok=True, data=result[0], message='success').to_json(),
            status=200,
            content_type='application/json'
        )

    def route(self):
        @self.http.route('/vaccination', methods=['GET'])
        def _getGeneralInformationVaccination():
            return self.getGeneralInformation()

        @self.http.route('/vaccination/yearly', methods=['GET'])
        def _getYearlyDataVaccination():
            return self.getYearlyData()

        @self.http.route('/vaccination/yearly/<year>')
        def _getDataByYearVaccination(year):
            return self.getDataByYear(year)

        @self.http.route('/vaccination/monthly', methods=['GET'])
        def _getMonthlyDataVaccination():
            return self.getMonthlyData()

        @self.http.route('/vaccination/monthly/<year>', methods=['GET'])
        def _getMonthlyDataByYearVaccination(year):
            return self.getMonthlyDataByYear(year)

        @self.http.route('/vaccination/monthly/<year>/<month>', methods=['GET'])
        def _getMonthlyDataByYearMonthVaccination(year, month):
            return self.getMonthlyDataByYearMonth(year, month)

        @self.http.route('/vaccination/daily', methods=['GET'])
        def _getDailyDataVaccination():
            return self.getDailyData()

        @self.http.route('/vaccination/daily/<year>', methods=['GET'])
        def _getDailyDataByYearVaccination(year):
            return self.getDailyDataByYear(year)

        @self.http.route('/vaccination/daily/<year>/<month>', methods=['GET'])
        def _getDailyDataInYearMonthVaccination(year, month):
            return self.getDailyDataInYearMonth(year, month)

        @self.http.route('/vaccination/daily/<year>/<month>/<date>', methods=['GET'])
        def _getDailyDataByDateVaccination(year, month, date):
            return self.getDailyDataByDate(year, month, date)
