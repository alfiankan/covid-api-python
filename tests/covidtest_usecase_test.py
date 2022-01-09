import sqlite3
from entites.covid_testing_data_entity import TotalCovidTestData, YearlyCovidTestData
from repositories.CovidTestDataRepository import CovidTestDataRepository
from usecases.CovidTestUseCase import CovidTestUseCase


def _useCase():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidTestDataRepository(db)
    return CovidTestUseCase(repo)


def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getGeneralInformation()
    assert isinstance(result, TotalCovidTestData)
    assert err is None


def testGetYearlyCase():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getYearlyDatasList(2025, 2030)
    assert err is None


def testGetCaseByYear():
    """Positive Test Get total case all time
    """
    useCase = _useCase()
    result, err = useCase.getDataByYear(2022)
    print(err)
    isinstance(result, YearlyCovidTestData)
    assert err is None
    assert result.antigen > 0


def testGetMonthlyCasesAll():
    """Positive Test get all monthly Data"""
    useCase = _useCase()
    result, err = useCase.getMonthlyData('2021.06', '2021.12')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert err is None


def testGetDailyCasesAll():
    """Positive Test get all monthly Data"""
    useCase = _useCase()
    result, err = useCase.getDailyData('2021.06.01', '2021.06.20')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert err is None
