from repositories.MinistryDataRepository import MinistryDataRepository
from repositories.VaccinationDataRepository import VaccinationDataRepository
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

class VaccinationUseCase():
    """
    UseData class hold VaccinationUseCase.
    this class returning defined entity
    and represent as App Level API

    Attributes
    ----------
    vaccRepository : VaccinationDataRepository
        local database repository object (act like cache)
    ministryRepository : MinistryDataRepository
        source data repository object
    """
    def __init__(self, vaccRepository: VaccinationDataRepository, ministryRepository: MinistryDataRepository = None):
        # init repository deps
        self._vaccRepository = vaccRepository
        self._ministryRepository = ministryRepository


    def getGeneralInformation(self):
        """
        Entry point, provide general information of covid Datas.

                Returns:
                        (Total): Total class object, contain total Data and last data
                        (error): return error
        """
        # get data from repository
        data, err = self._vaccRepository.getLastUpdateSummary()
        return data, err


    def getYearlyDatasList(self, since: int = 2020, upto: int = datetime.now().year):
        """Provide yearly data of total covid Datas. by default between starting Data (2020) until current year

            Parameters:
                        since (int): parameter to control since when (year) the data will be returned, default 2020 if empty
                        upto (int): parameter to control up to when (year) the data will be returned, by default up to the current year if empty
            Returns:
                        (list[YearlyVaccinationData]): yearly Data result data
                        (error): return error
        """
        # get data from repository
        yearlyResult, err = self._vaccRepository.getYearlyData(since, upto)
        return yearlyResult, err


    def getDataByYear(self, year: int):
        """Provide Data by year

            Parameters:
                        year (int): year
            Returns:
                        (YearlyVaccinationData): yearly Data result data
                        (error): return error
        """
        # get data from repository
        result, err = self._vaccRepository.getDataByYear(year)
        return result, err


    def syncDataWithApiSource(self):
        """updating local database with covid19 source data from trusted source (goverment)

            Returns:
                        (error): return error , return none if has no error
        """
        # check if dependency exist
        if self._ministryRepository == None:
            return "You need MinistryDataRepository Dependency"

        # get source data from ministry repository api
        sourceData, _,  err = self._ministryRepository.getDailyTestAndVaccinationData()
        if err != None:
            return err
        else:
            # if no error update data
            self._vaccRepository.truncateData()
            self._vaccRepository.bulkInsertDailyData(sourceData)


    def getMonthlyData(self, since: str = '2020.01', upto: str = datetime.utcfromtimestamp(time.time()).strftime("%Y.%m")):
        """Provide Data monthly if empty return all monthly data

            Parameters:
                        since (str): since month with format %Y.%m (eg. 2021.01)
                        upto (str): upto month with format %Y.%m (eg. 2021.01)
            Returns:
                        (MonthlyDatas): yearly Data result data
                        (error): return error
        """
        # validate since and upto match %Y.%m
        try:
            # convert string year.moth to timestamp
            sinceTimeStamp = time.mktime(datetime.strptime(since, "%Y.%m").timetuple())
            uptoTimeStamp = time.mktime((datetime.strptime(upto, "%Y.%m") + relativedelta(months=1)).timetuple())

            # get data from repository
            result, err = self._vaccRepository.getMonthlyData(sinceTimeStamp, uptoTimeStamp)
            return result, err

        except ValueError as e:
            return None, e


    def getDailyData(self, since: str = '2020.01.01', upto: str = datetime.utcfromtimestamp(time.time()).strftime("%Y.%m.%d")):
        """Provide Data monthly if empty return all daily data

            Parameters:
                        since (str): since month with format %Y.%m.%d (eg. 2021.01.01)
                        upto (str): upto month with format %Y.%m.%d (eg. 2021.01.01)
            Returns:
                        (DailyData): yearly Data result data
                        (error): return error
        """
        # validate since and upto match %Y.%m
        try:
            # convert string year.moth to timestamp
            sinceTimeStamp = time.mktime(datetime.strptime(since, "%Y.%m.%d").timetuple())
            uptoTimeStamp = time.mktime((datetime.strptime(upto, "%Y.%m.%d") + relativedelta(days=1)).timetuple())

            # get data from repository
            result, err = self._vaccRepository.getDailyData(sinceTimeStamp, uptoTimeStamp)
            return result, err

        except ValueError as e:
            return None, e
