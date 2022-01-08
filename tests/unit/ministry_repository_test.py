from entites.covid_data_entity import DailyCase
from entites.vaccination_data_entity import DailyVaccinationData
from repositories.MinistryDataRepository import MinistryDataRepository


def testGetDailyCaseData():
    repo = MinistryDataRepository()
    res, err = repo.getDailyCases()
    assert len(res) > 0
    assert err == None
    assert isinstance(res[0], DailyCase)


def testGetDailyVaccinationData():
    repo = MinistryDataRepository()
    resVacc, resTest, err = repo.getDailyTestAndVaccinationData()
    print('err', err)
    for x in resVacc:
        print(x)
    for y in resTest:
        print(y)
    assert len(resVacc) > 0
    assert len(resTest) > 0
    assert err == None
    assert isinstance(resVacc[0], DailyVaccinationData)
