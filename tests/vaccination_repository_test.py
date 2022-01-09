from sqlite3.dbapi2 import OperationalError
from entites.vaccination_data_entity import DailyVaccinationData, TotalVaccinationData, YearlyVaccinationData, MonthlyVaccinationData
from repositories.VaccinationDataRepository import VaccinationDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import sqlite3
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


def _repository():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    return VaccinationDataRepository(db)


def testGetTotalCasesAllTimeNegative():
    """Negative Test Get total case all time if repository error
    """
    db = sqlite3.connect('covid_database.dbl', isolation_level=None)
    repo = VaccinationDataRepository(db)
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err is not None
    assert isinstance(err, OperationalError)


def testGetTotalCasesAllTime():
    """Positive Test Get total case all time
    """
    repo = _repository()
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err is None
    assert isinstance(res, TotalVaccinationData)


def testGetDatabaseDataYearly():
    """Positive Test Get Data yearly
    """
    repo = _repository()
    res, _ = repo.getYearlyData(2020, 2023)

    assert isinstance(res[0], YearlyVaccinationData)


def testTruncate():
    """Positive Test Gdelete data all
    """
    repo = _repository()
    err = repo.truncateData()
    assert err is None


def testSyncData():
    """Positive sync with source data
    """
    repo = _repository()
    ministryRepo = MinistryDataRepository()
    repo.truncateData()

    vaccData, _, _ = ministryRepo.getDailyTestAndVaccinationData()

    err = repo.bulkInsertDailyData(vaccData)
    assert err is None


def testGetCaseByYear():
    """Positive Test Get total case all time
    """
    repo = _repository()
    res, err = repo.getDataByYear(2022)
    print(res)
    assert err is None
    assert isinstance(res, YearlyVaccinationData)
    assert res.first_vacc > 0


def testGetMonthlyDataWithRange():
    """Positive Test Get case monthly range
    """
    since = time.mktime(datetime.strptime("2021.02", "%Y.%m").timetuple())
    upto = time.mktime((datetime.strptime("2021.05", "%Y.%m") + relativedelta(months=1)).timetuple())
    repo = _repository()
    res, err = repo.getMonthlyData(since, upto)

    for c in res:
        print(c)

    print(type(res))
    assert err is None
    assert isinstance(res, list)
    assert isinstance(res[0], MonthlyVaccinationData)


def testGetDailyData():
    """Positive Test Get daily Data data
    """
    since = time.mktime(datetime.strptime("2021.02.01", "%Y.%m.%d").timetuple())
    upto = time.mktime((datetime.strptime("2021.02.10", "%Y.%m.%d") + relativedelta(days=1)).timetuple())
    repo = _repository()
    res, err = repo.getDailyData(since, upto)
    assert err is None
    assert isinstance(res[0], DailyVaccinationData)
    assert len(res) > 0
