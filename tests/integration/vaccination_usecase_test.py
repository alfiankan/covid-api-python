import sqlite3
from entites.vaccination_data_entity import TotalVaccinationData, YearlyVaccinationData
from repositories.CovidDataRepository import CovidDataRepository
from repositories.VaccinationDataRepository import VaccinationDataRepository
from usecases.VaccinationUseCase import VaccinationUseCase

def _useCase():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = VaccinationDataRepository(db)
    return VaccinationUseCase(repo)


def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getGeneralInformation()
    assert isinstance(result, TotalVaccinationData)
    assert err == None


def testGetYearlyCase():
    """Positive Test Get general Info
    """
    useCase = _useCase()
    result, err = useCase.getYearlyDatasList(2025, 2030)
    assert err == None


def testGetCaseByYear():
    """Positive Test Get total case all time
    """
    useCase = _useCase()
    result, err = useCase.getDataByYear(2022)
    isinstance(result, YearlyVaccinationData)
    assert err == None
    assert result.first_vacc > 0


def testGetMonthlyCasesAll():
    """Positive Test get all monthly Data"""
    useCase = _useCase()
    result, err = useCase.getMonthlyData('2021.06','2021.12')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert err == None


def testGetDailyCasesAll():
    """Positive Test get all monthly Data"""
    useCase = _useCase()
    result, err = useCase.getDailyData('2021.06.01','2021.06.20')
    for x in result:
        print(x)
    assert isinstance(result, list)
    assert err == None
