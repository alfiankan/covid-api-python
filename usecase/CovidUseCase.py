from datetime import datetime
from entity.CovidDataEntity import YearlyCase
from repository.CovidDataRepository import CovidDataRepository


class CovidUseCase():
    """
    UseCase class hold CovidUseCase Business Logic.

    Attributes
    ----------
    covidRepository : CovidDataRepository
        repository object
    """
    def __init__(self, covidRepository: CovidDataRepository):
        self._covidRepository = covidRepository

    def getGeneralInformation(self):
        ## TODO : handle if main source api error -> use cache
        data, err = self._covidRepository.getLastUpdateSummary()
        return data, err

    def getYearlyCasesList(self, since: int, upto: int):
        """Provide yearly data of total covid cases. by default between starting case (2020) until current year

        Args:
            since (int): parameter to control since when (year) the data will be returned, default 2020
            upto (int): parameter to control up to when (year) the data will be returned, by default up to the current year.
        """


        dailyData, err = self._covidRepository.getDailyCases()
        # TODO: handle error

        yearlyResult = list()
        ## filter daily data by year
        for year in range(since, upto + 1):
            positive: int = 0
            recovered: int = 0
            death: int = 0
            active: int = 0

            for covidCase in dailyData:
                # assert if match year increment calculation
                if datetime.utcfromtimestamp(covidCase.date).year == year:
                    positive += covidCase.positive
                    recovered += covidCase.recovered
                    death += covidCase.death
                    active += covidCase.active

            # append calculation result
            yearlyResult.append(YearlyCase(year, positive, recovered, death, active))

        return yearlyResult, err

    def getYearlyCasesDetail(self):
        pass
