import sqlite3
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase


def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    pass


def testGetYearlyCase():
    """Positive Test Get general Info
    """
    db = sqlite3.connect('covid_database.db')
    repo = CovidDataRepository(db)
    useCase = CovidUseCase(repo)
    result, err = useCase.getYearlyCasesList(2025, 2030)
    print(result)
    assert err == None
