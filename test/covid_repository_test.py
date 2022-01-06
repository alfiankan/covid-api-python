from entity.CovidDataEntity import TotalCase
from repository.CovidDataRepository import CovidDataRepository

def testGetLastUpdatedData():
    """Positive Test Get Last Updated Data From Repository
    """
    repo = CovidDataRepository()
    result, err = repo.getUpdateData()
    print(result)
    # must instance of TotalCase Entity
    assert err == None
    assert isinstance(result, TotalCase)
