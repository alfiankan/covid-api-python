from sqlite3.dbapi2 import OperationalError
from entites.covid_data_entity import TotalCase, YearlyCase, MonthlyCase
from repositories.CovidDataRepository import CovidDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import sqlite3
import pytest
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


def _repository():
    """Helper dependency injection"""
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    return CovidDataRepository(db)


def testGetTotalCasesAllTimeNegative():
    """Negative Test Get total case all time if repository error
    """
    db = sqlite3.connect('covid_database.dbl', isolation_level=None)
    repo = CovidDataRepository(db)
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err != None
    assert isinstance(err, OperationalError)

def testGetTotalCasesAllTime():
    """Positive Test Get total case all time
    """
    repo = _repository()
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err == None
    assert isinstance(res, TotalCase)


def testGetDatabaseDataYearly():
    """Positive Test Get cases yearly
    """
    repo = _repository()
    res, _ = repo.getYearlyCases(2020, 2023)

    assert isinstance(res[0], YearlyCase)

def testTruncate():
    """Positive Test Gdelete data all
    """
    repo = _repository()
    err = repo.truncateData()
    assert err == None


def testSyncData():
    """Positive sync with source data
    """
    repo = _repository()
    ministryRepo = MinistryDataRepository()
    repo.truncateData()

    ministryData, _ = ministryRepo.getDailyCases()

    err = repo.bulkInsertDailyCaseData(ministryData)
    assert err == None



def testGetCaseByYear():
    """Positive Test Get total case all time
    """
    repo = _repository()
    res, err = repo.getCaseByYear(2022)
    print(res)
    assert err == None
    assert isinstance(res, YearlyCase)
    assert res.active > 0

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
    assert err == None
    assert isinstance(res, list)
    assert isinstance(res[0], MonthlyCase)


def testGetDailyData():
    """Positive Test Get daily cases data
    """
    since = time.mktime(datetime.strptime("2021.02.01", "%Y.%m.%d").timetuple())
    upto = time.mktime((datetime.strptime("2021.02.10", "%Y.%m.%d") + relativedelta(days=1)).timetuple())
    repo = _repository()
    res, err = repo.getDailyData(since, upto)
    print(res)
    assert err == None
    assert isinstance(res, YearlyCase)
    assert res.active > 0
