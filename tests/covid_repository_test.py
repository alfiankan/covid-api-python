from entity.CovidDataEntity import DailyCase, TotalCase
from repository.CovidDataRepository import CovidDataRepository
import datetime


def testGetLastUpdateSummary():
    """Positive Test Get Last Updated Data From Repository
    """
    repo = CovidDataRepository()
    result, err = repo.getLastUpdateSummary()
    print(result)
    # must instance of TotalCase Entity
    assert err == None
    assert isinstance(result, TotalCase)


def testGetDailyCases():
    """Positive Test Get Daily Cases
    """
    repo = CovidDataRepository()
    result, err = repo.getDailyCases()

    # must instance of TotalCase Entity
    assert err == None
    assert isinstance(result[0], DailyCase)
