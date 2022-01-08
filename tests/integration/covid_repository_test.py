from sqlite3.dbapi2 import OperationalError
from entites.CovidDataEntity import TotalCase, YearlyCase
from repositories.CovidDataRepository import CovidDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import sqlite3
import pytest

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
