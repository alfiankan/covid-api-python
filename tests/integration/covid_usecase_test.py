import sqlite3
from entites.covid_data_entity import TotalCase, YearlyCase
from repositories.CovidDataRepository import CovidDataRepository
from usecases.CovidUseCase import CovidUseCase

def _useCase():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidDataRepository(db)
    return CovidUseCase(repo)


def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getGeneralInformation()
    assert isinstance(result, TotalCase)
    assert err == None


def testGetYearlyCase():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getYearlyCasesList(2025, 2030)
    assert err == None


def testGetCaseByYear():
    """Positive Test Get total case all time
    """
    useCase = _useCase()
    result, err = useCase.getCaseByYear(2022)
    isinstance(result, YearlyCase)
    assert err == None
    assert result.active > 0


def testGetMonthlyCasesAll():
    """Positive Test get all monthly cases"""
    useCase = _useCase()
    result, err = useCase.getMonthlyCase('2021.06','2021.12')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert len(result) == 7
    assert err == None


def testGetDailyCasesAll():
    """Positive Test get all monthly cases"""
    useCase = _useCase()
    result, err = useCase.getDailyCase('2021.06.01','2021.06.20')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert len(result) == 20
    assert err == None
