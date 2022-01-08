from flask.app import Flask
import flask_unittest
import pytest
from http_server import startServer
import json

# TODO: simplyfy function name in test
def createFlaskTestApp():
    flaskApp = startServer()
    flaskApp.config["TESTING"] = True
    return flaskApp.test_client()

def testGetGeneralInformation():
    """[POSITIVE] Test Route / [get general information]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['ok'])
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert list(decodedJson['data'].keys()) == ['total_positive', 'total_recovered', 'total_death', 'total_active', 'new_positive', 'new_recovered', 'new_death', 'new_active']

def testGetYearlyData():
    """[POSITIVE] Test Route /yearly [get yearly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['year', 'positive', 'recovered', 'death', 'active']

def testGetYearlyDataWiyhRange():
    """[POSITIVE] Test Route /yearly?since=2020&upto=2021 [get yearly cases with year range]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly?since=2020&upto=2021')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) == 2 # only result 2020 and 2021
    assert decodedJson['data'][0]['year'] == '2020'
    assert decodedJson['data'][1]['year'] == '2021'
    assert list(decodedJson['data'][0].keys()) == ['year', 'positive', 'recovered', 'death', 'active']


def testGetYearlyDataWiyhRangeWrongQueryParamType():
    """[NEGATIVE] Test Route /yearly?since=abc&upto=2021 [get yearly cases with year range with alphabet]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly?since=abc&upto=2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, since Must be number integer'


def testGetYearlyDataWiyhRangeEmptyVSingleQueryParam():
    """[POSITIVE] Test Route /yearly?since=2020 [get yearly cases with year range with singlequery param]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly?since=2020')
    print(response.data)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert decodedJson['data'][0]['year'] == '2020'
    assert list(decodedJson['data'][0].keys()) == ['year', 'positive', 'recovered', 'death', 'active']



def testGetCaseDataByYearInParam():
    """[POSITIVE] Test Route /yearly/2021 [get yearly cases by year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly/2021')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert decodedJson['data']['year'] == '2021'
    assert list(decodedJson['data'].keys()) == ['year', 'positive', 'recovered', 'death', 'active']


def testGetCaseDataByYearInParamIfNotFound():
    """[NEGATIVE] Test Route /yearly/2029 [get yearly cases by year not found]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly/2029')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 404
    assert decodedJson['ok'] == False



def testGetCaseDataByYearInParamIfInvalidtype():
    """[NEGATIVE] Test Route /yearly/two [get yearly cases by year invalid type]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/yearly/two')
    print(response.data)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] ==  'Validation error, year Must be number integer'



def testGetMonthlyData():
    """[POSITIVE] Test Route /monthly?since=2021.05 [get monthly cases]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'positive', 'recovered', 'death', 'active']


def testGetMonthlyDataWithWrongDateType():
    """[NEGATIVE] Test Route /monthly?since=2021.054 [get monthly cases] with wrong param"""
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly?since=2021.054')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, since Must folow date format <year>.<month> eg. 2020.01'



def testGetMonthlyDataInSpesificYear():
    """[POSITIVE] Test Route /monthly/2021?since=2021.05 [get monthly cases in spesific year]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly/2021?since=2021.05')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    print(decodedJson['data'][0].keys())
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert len(decodedJson['data']) > 0
    assert list(decodedJson['data'][0].keys()) == ['month', 'positive', 'recovered', 'death', 'active']


def testGetMonthlyDataInSpesificYearWithWrongYearQueryParam():
    """[NEGATIVE] Test Route /monthly?since=2021.054 [get monthly cases] with wrong month format (mont is not in spesific year)"""
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly/2021?since=2020.04')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, month format request is not in year, make sure <year> in ?since=<year>.<month> and ?upto=<year>.<month>  /monthly/<year> is same year, (eg. monthly/2021?since=2021.05&upto=2021.09)'

def testGetMonthlySingleDataInSpesificYearMonth():
    """[POSITIVE] Test Route /monthly/2021/02 [get monthly cases in spesific year and month]"""
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly/2021/02')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 200
    assert decodedJson['ok'] == True
    assert list(decodedJson['data'].keys()) == ['month', 'positive', 'recovered', 'death', 'active']


def testGetMonthlySingleDataInSpesificYearMonthWithWrongParamFormat():
    """[NEGATIVE] Test Route /monthly/2021/39 [get monthly cases] with wrong format """
    testApp = createFlaskTestApp()
    response = testApp.get('/monthly/2021/39')
    print(response.status_code)
    decodedJson = json.loads(response.data)
    assert response.status_code == 422
    assert decodedJson['ok'] == False
    assert decodedJson['message'] == 'Validation error, upto Must folow date format <year>.<month> eg. 09'
