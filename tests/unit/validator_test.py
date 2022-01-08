



from validation.http_api_validation import isValidationError, validateIsNotEmpty, validateIsNumber, validateIsTypeValid, validationErrMessage

def testIsTypeValid():
    """[UNIT] test case string is float"""
    valErr = validateIsTypeValid('1', float, 'input')
    print(valErr)
    assert valErr != None

def testIsEmpty():
    """[UNIT] test case '' is empty string"""
    valErr = validateIsNotEmpty('', 'input')
    assert valErr == "input Must be not empty"

def testValidateIsNumber():
    """[UNIT] test case 'r' is number"""
    vallErr = validateIsNumber('r', 'input')
    assert vallErr == "input Must be number integer"

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
    assert isError == True
