from validation.http_api_validation import isValidationError, validateIsNotEmpty, validateIsNumber, validateIsTypeValid, validateIsmatchDateFormat, validationErrMessage


def testIsTypeValid():
    """[UNIT] test case string is float"""
    valErr = validateIsTypeValid('1', float, 'input')
    print(valErr)
    assert valErr is not None


def testIsEmpty():
    """[UNIT] test case '' is empty string"""
    valErr = validateIsNotEmpty('', 'input')
    assert valErr == "input Must be not empty"


def testValidateIsNumber():
    """[UNIT] test case 'r' is number"""
    vallErr = validateIsNumber('r', 'input')
    assert 'input Must be number integer' in vallErr


def testValidationErrMessage():
    """[UNIT] test convert list error to one line message"""
    valErr1 = "input Must be not empty"
    valErr2 = "input Must be not empty"
    errMsg = validationErrMessage([valErr1, valErr2])
    assert errMsg == "input Must be not empty, input Must be not empty"


def testIsValidationError():
    """[UNIT] test convert validation error"""
    valErr1 = "input Must be not empty"
    valErr2 = "input Must be not empty"
    isError = isValidationError([valErr1, valErr2])
    assert isError is True


def testValidateDateInput():
    """[UNIT] validate is date string input match expected date format  """
    vallErr = validateIsmatchDateFormat('20204.02', '%Y.%m', 'since', '<year>.<month> eg. 2020.01')
    print(vallErr)
    assert vallErr == "since Must folow date format <year>.<month> eg. 2020.01"
