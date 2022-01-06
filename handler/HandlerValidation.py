

def validateIsEmptyQueryParam(data, fieldName):

    if data == '' or data == None:
        return "{} Must be not empty".format(fieldName)
    return None

def validateIsTypeValid(data, type, fieldName):
    if isinstance(data, type):
        return None
    return "{} Must be {}".format(fieldName, type)

def validateIsNumber(data, fieldName):
    try:
        res = int(data)
        return None
    except:
        return "{} Must be number integer".format(fieldName)

def validationErrMessage(valErr):
    return ", ".join(list(filter(None, valErr)))

def isValidationError(valError):
    if valError != [None for x in range(len(valError))]:
        return True
    return False

