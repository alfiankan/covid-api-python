from entity.CovidDataEntity import TotalCase, YearlyCase
from repository.CovidDataRepository import CovidDataRepository
from repository.MinistryDataRepository import MinistryDataRepository

import sqlite3

def testGetLastUpdateSummary():
    """Positive Test Get Last Updated Data From Repository
    """
    pass

def testGetTotalCasesAllTime():
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidDataRepository(db)
    res, err = repo.getLastUpdateSummary()
    print(res)
    assert err == None
    assert isinstance(res, TotalCase)


def testGetDatabaseDataYearly():
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidDataRepository(db)
    res, err = repo.getYearlyCases(2020, 2023)

    assert isinstance(res[0], YearlyCase)

def testTruncate():
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidDataRepository(db)
    err = repo.truncateData()
    assert err == None

def testSyncData():
    db = sqlite3.connect('covid_database.db', isolation_level=None)
    repo = CovidDataRepository(db)
    ministryRepo = MinistryDataRepository()
    repo.truncateData()

    ministryData, _ = ministryRepo.getDailyCases()

    err = repo.bulkInsertDailyCaseData(ministryData)
    assert err == None
