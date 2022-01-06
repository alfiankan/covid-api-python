from repository.CovidDataRepository import CovidDataRepository


class CovidUseCase():
    def __init__(self, covidRepository: CovidDataRepository):
        self._covidRepository = covidRepository

    def getGeneralInformation(self):
        ## TODO : handle if main source api error -> use cache
        data, err = self._covidRepository.getUpdateData()
        return data, err

    def getYearlyCasesList(self, since: int, upto: int):
        """Provide yearly data of total covid cases. by default between starting case (2020) until current year

        Args:
            since (int): parameter to control since when (year) the data will be returned, default 2020
            upto (int): parameter to control up to when (year) the data will be returned, by default up to the current year.
        """
        pass

    def getYearlyCasesDetail(self):
        pass
