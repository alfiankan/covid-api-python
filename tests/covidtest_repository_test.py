from sqlite3.dbapi2 import OperationalError
from entites.covid_testing_data_entity import DailyCovidTestData, TotalCovidTestData, YearlyCovidTestData, MonthlyCovidTestData
from repositories.CovidTestDataRepository import CovidTestDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import sqlite3
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


def _repository():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    return CovidTestDataRepository(db)


def testGetTotalDatasAllTimeNegative():
    """Negative Test Get total Data all time if repository error
    """
    db = sqlite3.connect('covid_database.dbl', isolation_level=None)
    repo = CovidTestDataRepository(db)
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err is not None
    assert isinstance(err, OperationalError)


def testGetTotalDatasAllTime():
    """Positive Test Get total Data all time
    """
    repo = _repository()
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err is None
    assert isinstance(res, TotalCovidTestData)


def testGetDatabaseDataYearly():
    """Positive Test Get Data yearly
    """
    repo = _repository()
    res, _ = repo.getYearlyData(2020, 2023)

    assert isinstance(res[0], YearlyCovidTestData)


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

    _, data, _ = ministryRepo.getDailyTestAndVaccinationData()
    err = repo.bulkInsertDailyData(data)
    print(err)
    assert err is None


def testGetDataByYear():
    """Positive Test Get total Data all time
    """
    repo = _repository()
    res, err = repo.getDataByYear(2022)
    print(res)
    assert err is None
    assert isinstance(res, YearlyCovidTestData)
    assert res.pcr_tcm > 0


def testGetMonthlyDataWithRange():
    """Positive Test Get Data monthly range
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
    assert isinstance(res[0], MonthlyCovidTestData)


def testGetDailyData():
    """Positive Test Get daily Data data
    """
    since = time.mktime(datetime.strptime("2021.02.01", "%Y.%m.%d").timetuple())
    upto = time.mktime((datetime.strptime("2021.02.20", "%Y.%m.%d") + relativedelta(days=1)).timetuple())
    repo = _repository()
    res, err = repo.getDailyData(since, upto)
    print(res)
    assert err is None
    #assert isinstance(res[0], DailyCovidTestData)
    assert len(res) > 0
