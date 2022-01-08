from api import startApi
import json

def createFlaskTestApp():
    flaskApp = startApi()
    flaskApp.config["TESTING"] = True
    return flaskApp.test_client()

def testGetGeneralInformation():
    """[POSITIVE] Test Route /vaccination [get general information]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['ok'])
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert list(decodedJson['data'].keys()) == ['first_vacc', 'second_vacc']

def testGetYearlyData():
    """[POSITIVE] Test Route /vaccination/yearly [get yearly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['year', 'first_vacc', 'second_vacc']

def testGetYearlyDataWiyhRange():
    """[POSITIVE] Test Route /vaccination/yearly?since=2020&upto=2021 [get yearly cases with year range]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly?since=2020&upto=2021')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    print(decodedJson['data'])
    assert list(decodedJson['data'][0].keys()) == ['year', 'first_vacc', 'second_vacc']


def testGetYearlyDataWiyhRangeWrongQueryParamType():
    """[NEGATIVE] Test Route /vaccination/yearly?since=abc&upto=2021 [get yearly cases with year range with alphabet]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly?since=abc&upto=2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False


def testGetYearlyDataWiyhRangeEmptyVSingleQueryParam():
    """[POSITIVE] Test Route /vaccination/yearly?since=2020 [get yearly cases with year range with singlequery param]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly?since=2020')
    print(response.data)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['year', 'first_vacc', 'second_vacc']



def testGetCaseDataByYearInParam():
    """[POSITIVE] Test Route /vaccination/yearly/2021 [get yearly cases by year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly/2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert decodedJson['data']['year'] == '2021'
    assert list(decodedJson['data'].keys()) == ['year', 'first_vacc', 'second_vacc']


def testGetCaseDataByYearInParamIfNotFound():
    """[NEGATIVE] Test Route /vaccination/yearly/2029 [get yearly cases by year not found]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly/2029')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 404
    assert decodedJson['ok'] == False



def testGetCaseDataByYearInParamIfInvalidtype():
    """[NEGATIVE] Test Route /vaccination/yearly/two [get yearly cases by year invalid type]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/yearly/two')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False



def testGetMonthlyData():
    """[POSITIVE] Test Route /vaccination/monthly?since=2021.05 [get monthly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'first_vacc', 'second_vacc']


def testGetMonthlyDataWithWrongDateType():
    """[NEGATIVE] Test Route /vaccination/monthly?since=2021.054 [get monthly cases] with wrong param"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly?since=2021.054')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month> eg. 2020.01  and cant be empty'



def testGetMonthlyDataInSpesificYear():
    """[POSITIVE] Test Route /vaccination/monthly/2021?since=2021.05 [get monthly cases in spesific year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly/2021?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'first_vacc', 'second_vacc']


def testGetMonthlyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /vaccination/monthly?since=2021.054 [get monthly cases] with wrong month format (mont is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly/2021?since=2020.04')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)'

def testGetMonthlySingleDataInSpesificYearMonth():
    """[POSITIVE] Test Route /vaccination/monthly/2021/02 [get monthly cases in spesific year and month]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly/2021/02')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert list(decodedJson['data'].keys()) == ['month', 'first_vacc', 'second_vacc']


def testGetMonthlySingleDataInSpesificYearMonthWithWrongParamFormat():
    """[NEGATIVE] Test Route /vaccination/monthly/2021/39 [get monthly cases] with wrong format """
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly/2021/39')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, upto Must folow date format <year>.<month> eg. 09  and cant be empty'


def testGetDailyData():
    """[POSITIVE] Test Route /vaccination/daily?since=2021.05.01 [get daily cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['date', 'first_vacc', 'second_vacc']


def testGetDailyDataWithWrongDateType():
    """[NEGATIVE] Test Route /vaccination/daily?since=2021.054 [get daily cases] with wrong param"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily?since=2021.054')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month> eg. 2020.01.01 and cant be empty'



def testGetDailyDataInSpesificYear():
    """[POSITIVE] Test Route /vaccination/daily/2021?since=2021.05.01 [get daily cases in spesific year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily/2021?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['date', 'first_vacc', 'second_vacc']


def testGetDailyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /vaccination/monthly?since=2021.059.03 [get daily cases] with wrong date format (date is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/monthly/2021?since=2020.04')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)'


def testGetDailySingleDataInSpesificYearMonth():
    """[POSITIVE] Test Route /vaccination/daily/2021/02 [get daily cases in spesific date]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily/2021/02')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert list(decodedJson['data'][0].keys()) == ['date', 'first_vacc', 'second_vacc']


def testGetDailySingleDataInSpesificYearMonthWithWrongParamFormat():
    """[NEGATIVE] Test Route /vaccination/daily/2021/39 [get daily cases] with wrong format """
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily/2021/39')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, make sure year month and date in 2021.01.01 date format'



def testGetDailyDataInSpesificYear():
    """[POSITIVE] Test Route /vaccination/daily/2021/05?since=2021.05.01 [get daily cases in spesific year month]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily/2021/05?since=2021.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['date', 'first_vacc', 'second_vacc']


def testGetDailyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /vaccination/daily/2021/05?since=2021e.05.01 [get daily cases] with wrong month format (mont is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/vaccination/daily/2021/05?since=2021e.05.01')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month>.<date> eg. 2020.01.01  and cant be empty'
