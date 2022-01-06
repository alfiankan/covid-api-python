


from logging import error

from handler.HandlerValidation import validateIsTypeValid




def testIsTypeValid():
    valErr = validateIsTypeValid('1', float, 'input')
    print(valErr)
    assert valErr != None
