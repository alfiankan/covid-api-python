from api import app
import json


def createFlaskTestApp():
    flaskApp = app
    flaskApp.config["TESTING"] = True
    return flaskApp.test_client()


def testGetGeneralInformation():
    """[POSITIVE] Test Route /test [get general information]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['ok'])
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    print(decodedJson['data'].keys())
    assert list(decodedJson['data'].keys()) == ['total_pcr_tcm_specimen', 'total_antigen_specimen', 'total_antigen', 'total_pcr_tcm', 'new_pcr_tcm_specimen', 'new_antigen_specimen', 'new_antigen', 'new_pcr_tcm']


def testGetYearlyData():
    """[POSITIVE] Test Route /test/yearly [get yearly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['year', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetYearlyDataWiyhRange():
    """[POSITIVE] Test Route /test/yearly?since=2020&upto=2021 [get yearly cases with year range]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly?since=2020&upto=2021')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    print(decodedJson['data'])
    assert list(decodedJson['data'][0].keys()) == ['year', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetYearlyDataWiyhRangeWrongQueryParamType():
    """[NEGATIVE] Test Route /test/yearly?since=abc&upto=2021 [get yearly cases with year range with alphabet]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly?since=abc&upto=2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False


def testGetYearlyDataWiyhRangeEmptyVSingleQueryParam():
    """[POSITIVE] Test Route /test/yearly?since=2020 [get yearly cases with year range with singlequery param]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly?since=2020')
    print(response.data)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['year', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetCaseDataByYearInParam():
    """[POSITIVE] Test Route /test/yearly/2021 [get yearly cases by year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly/2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert decodedJson['data']['year'] == '2021'
    assert list(decodedJson['data'].keys()) == ['year', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetCaseDataByYearInParamIfNotFound():
    """[NEGATIVE] Test Route /test/yearly/2029 [get yearly cases by year not found]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly/2029')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 404
    assert decodedJson['ok'] is False


def testGetCaseDataByYearInParamIfInvalidtype():
    """[NEGATIVE] Test Route /test/yearly/two [get yearly cases by year invalid type]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/yearly/two')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False


def testGetMonthlyData():
    """[POSITIVE] Test Route /test/monthly?since=2021.05 [get monthly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetMonthlyDataWithWrongDateType():
    """[NEGATIVE] Test Route /test/monthly?since=2021.054 [get monthly cases] with wrong param"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly?since=2021.054')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month> eg. 2020.01  and cant be empty'


def testGetMonthlyDataInSpesificYear():
    """[POSITIVE] Test Route /test/monthly/2021?since=2021.05 [get monthly cases in spesific year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly/2021?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetMonthlyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /test/monthly?since=2021.054 [get monthly cases] with wrong month format (mont is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly/2021?since=2020.04')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)'


def testGetMonthlySingleDataInSpesificYearMonth():
    """[POSITIVE] Test Route /test/monthly/2021/05 [get monthly cases in spesific year and month]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly/2021/05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert list(decodedJson['data'].keys()) == ['month', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetMonthlySingleDataInSpesificYearMonthWithWrongParamFormat():
    """[NEGATIVE] Test Route /test/monthly/2021/39 [get monthly cases] with wrong format """
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly/2021/39')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, upto Must folow date format <year>.<month> eg. 09  and cant be empty'


def testGetDailyData():
    """[POSITIVE] Test Route /test/daily?since=2021.05.01 [get daily cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['date', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetDailyDataWithWrongDateType():
    """[NEGATIVE] Test Route /test/daily?since=2021.054 [get daily cases] with wrong param"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily?since=2021.054')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month> eg. 2020.01.01 and cant be empty'


def testGetDailyDataInSpesificYear():
    """[POSITIVE] Test Route /test/daily/2021?since=2021.05.01 [get daily cases in spesific year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily/2021?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['date', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetDailyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /test/monthly?since=2021.059.03 [get daily cases] with wrong date format (date is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/monthly/2021?since=2020.04')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)'


def testGetDailySingleDataInSpesificYearMonth():
    """[POSITIVE] Test Route /test/daily/2021/05 [get daily cases in spesific date]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily/2021/05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert list(decodedJson['data'][0].keys()) == ['date', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetDailySingleDataInSpesificYearMonthWithWrongParamFormat():
    """[NEGATIVE] Test Route /test/daily/2021/39 [get daily cases] with wrong format """
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily/2021/39')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, make sure year month and date in 2021.01.01 date format'


def testGetDailyVaccDataInSpesificYear():
    """[POSITIVE] Test Route /test/daily/2021/05?since=2021.05.01 [get daily cases in spesific year month]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily/2021/05?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] is True
    assert len(decodedJson['data']) > 0
    print(decodedJson['data'][0].keys())
    assert list(decodedJson['data'][0].keys()) == ['date', 'pcr_tcm_specimen', 'antigen_specimen', 'antigen', 'pcr_tcm']


def testGetDailyVaccDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /test/daily/2021/05?since=2021e.05.01 [get daily cases] with wrong month format (mont is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/test/daily/2021/05?since=2021e.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] is False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month>.<date> eg. 2020.01.01  and cant be empty'
