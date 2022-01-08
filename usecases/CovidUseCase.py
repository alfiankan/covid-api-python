import datetime
from entites.CovidDataEntity import YearlyCase
from repositories.MinistryDataRepository import MinistryDataRepository
from repositories.CovidDataRepository import CovidDataRepository

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

    def getYearlyCasesList(self, since: int = 2020, upto: int = datetime.datetime.now().year):
        """Provide yearly data of total covid cases. by default between starting case (2020) until current year

            Args:
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

            Args:
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
        self._covidRepository.truncateData()
        self._covidRepository.bulkInsertDailyCaseData(sourceData)

    def getYearlyCasesDetail(self):
        pass
