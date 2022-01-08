
from typing import Any, List
import time
from datetime import datetime
def validateIsNotEmpty(data: str, fieldName: str):
    """Validate if data empty"""
    if data == '' or data == None:
        return "{} Must be not empty".format(fieldName)
    return None

def validateIsTypeValid(data: Any, type: Any, fieldName: str):
    """Validate if type instanceof target"""
    if isinstance(data, type):
        return None
    return "{} Must be {}".format(fieldName, type)

def validateIsNumber(data: Any, fieldName: str):
    """Validate if able to be int, and can't be empty'"""
    try:
        res = int(data)
        return None
    except:
        return "{} Must be number integer,  and cant be empty'".format(fieldName)

def validationErrMessage(valErr: List[str]):
    """returning list error as one line message"""
    return ", ".join(list(filter(None, valErr)))

def isValidationError(valError: List[str]):
    """Validate all error validation"""
    if valError != [None for x in range(len(valError))]:
        return True
    return False

def validateIsmatchDateFormat(date: str, dateFormat: str, fieldName: str, readableFormat: str = '', ):
    """Validate date format from string"""
    try:
        # convert string year.moth to timestamp
        sinceTimeStamp = time.mktime(datetime.strptime(date, dateFormat).timetuple())
        return None
    except ValueError as e:
        return "{} Must folow date format {}".format(fieldName, readableFormat)

