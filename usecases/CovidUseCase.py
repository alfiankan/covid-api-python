from entites.covid_data_entity import YearlyCase
from repositories.MinistryDataRepository import MinistryDataRepository
from repositories.CovidDataRepository import CovidDataRepository
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

class CovidUseCase():
    """
    UseCase class hold CovidUseCase.
    this class returning defined entity
    and represent as App Level API

    Attributes
    ----------
    covidRepository : CovidDataRepository
        local database repository object (act like cache)
    ministryRepository : MinistryDataRepository
        source data repository object
    """
    def __init__(self, covidRepository: CovidDataRepository, ministryRepository: MinistryDataRepository = None):
        # init repository deps
        self._covidRepository = covidRepository
        self._ministryRepository = ministryRepository


    def getGeneralInformation(self):
        """
        Entry point, provide general information of covid cases.

                Returns:
                        (TotalCase): TotalCase class object, contain total case and last case
                        (error): return error
        """
        data, err = self._covidRepository.getLastUpdateSummary()
        return data, err


    def getYearlyCasesList(self, since: int = 2020, upto: int = datetime.now().year):
        """Provide yearly data of total covid cases. by default between starting case (2020) until current year

            Parameters:
                        since (int): parameter to control since when (year) the data will be returned, default 2020 if empty
                        upto (int): parameter to control up to when (year) the data will be returned, by default up to the current year if empty
            Returns:
                        (list[YearlyCase]): yearly case result data
                        (error): return error
        """

        yearlyResult, err = self._covidRepository.getYearlyCases(since, upto)
        return yearlyResult, err


    def getCaseByYear(self, year: int):
        """Provide case by year

            Parameters:
                        year (int): year
            Returns:
                        (YearlyCase): yearly case result data
                        (error): return error
        """

        result, err = self._covidRepository.getCaseByYear(year)
        return result, err


    def syncDataWithApiSource(self):
        """updating local database with covid19 source data from trusted source (goverment)

            Returns:
                        (error): return error , return none if has no error
        """
        if self._ministryRepository == None:
            return "You need MinistryDataRepository Dependency"
        sourceData, err = self._ministryRepository.getDailyCases()
        if err != None:
            return err
        else:
            self._covidRepository.truncateData()
            self._covidRepository.bulkInsertDailyCaseData(sourceData)


    def getMonthlyCase(self, since: str = '2020.01', upto: str = datetime.utcfromtimestamp(time.time()).strftime("%Y.%m")):
        """Provide case monthly if empty return all monthly data

            Parameters:
                        since (str): since month with format %Y.%m (eg. 2021.01)
                        upto (str): upto month with format %Y.%m (eg. 2021.01)
            Returns:
                        (MonthlyCases): yearly case result data
                        (error): return error
        """
        # validate since and upto match %Y.%m
        try:
            # convert string year.moth to timestamp
            sinceTimeStamp = time.mktime(datetime.strptime(since, "%Y.%m").timetuple())
            uptoTimeStamp = time.mktime((datetime.strptime(upto, "%Y.%m") + relativedelta(months=1)).timetuple())

            # get data from repository
            result, err = self._covidRepository.getMonthlyData(sinceTimeStamp, uptoTimeStamp)

            return result, err
        except ValueError as e:
            return None, e


    def getDailyCase(self, since: str = '2020.01.01', upto: str = datetime.utcfromtimestamp(time.time()).strftime("%Y.%m.%d")):
        """Provide case monthly if empty return all daily data

            Parameters:
                        since (str): since month with format %Y.%m.%d (eg. 2021.01.01)
                        upto (str): upto month with format %Y.%m.%d (eg. 2021.01.01)
            Returns:
                        (DailyCase): yearly case result data
                        (error): return error
        """
        # validate since and upto match %Y.%m
        try:
            # convert string year.moth to timestamp
            sinceTimeStamp = time.mktime(datetime.strptime(since, "%Y.%m.%d").timetuple())
            uptoTimeStamp = time.mktime((datetime.strptime(upto, "%Y.%m.%d") + relativedelta(days=1)).timetuple())

            # get data from repository
            result, err = self._covidRepository.getDailyData(sinceTimeStamp, uptoTimeStamp)

            return result, err
        except ValueError as e:
            return None, e
