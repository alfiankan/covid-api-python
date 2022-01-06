from entity.CovidDataEntity import TotalCase
from repository.CovidDataRepository import CovidDataRepository
from usecase.CovidUseCase import CovidUseCase

def testGetGeneralInformation():
    """Positive Test Get general Info
    """
    repo = CovidDataRepository()
    useCase = CovidUseCase(repo)
    result, err = useCase.getGeneralInformation()
    print(result)
    assert err == None
    assert isinstance(result, TotalCase)
