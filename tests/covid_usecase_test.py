from entity.CovidDataEntity import TotalCase, YearlyCase
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase

def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    repo = CovidDataRepository()
    useCase = CovidUseCase(repo)
    result, err = useCase.getGeneralInformation()
    print(result)
    assert err == None
    assert isinstance(result, TotalCase)


def testGetYearlyCase():
    """Positive Test Get general Info
    """
    repo = CovidDataRepository()
    useCase = CovidUseCase(repo)
    result, err = useCase.getYearlyCasesList(2020, 2021)
    print(result)
    assert err == None
    assert isinstance(result[0], YearlyCase)
