import sqlite3
from entites.CovidDataEntity import TotalCase
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
