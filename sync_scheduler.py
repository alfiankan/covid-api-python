import sqlite3
from repositories.CovidDataRepository import CovidDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import schedule
import time
from repositories.VaccinationDataRepository import VaccinationDataRepository

from usecases.CovidUseCase import CovidUseCase
from usecases.VaccinationUseCase import VaccinationUseCase

# DATABASE SYNC SCHEDULER ENTRY POINT
# create db object


def runSync():
    db = sqlite3.connect('covid_database.db', isolation_level=None, check_same_thread=False)

    ministryRepo = MinistryDataRepository()

    # scnc covid data
    covidRepo = CovidDataRepository(db)
    covid = CovidUseCase(covidRepo, ministryRepo)
    err = covid.syncDataWithApiSource()

    # scnc vaccination data
    vaccRepo = VaccinationDataRepository(db)
    vacc = VaccinationUseCase(vaccRepo, ministryRepo)
    err = vacc.syncDataWithApiSource()

    if err is None:
        print("Sync Success...")
    else:
        print(err)

runSync()
schedule.every(5).hours.do(runSync)
while True:
  schedule.run_pending()
  time.sleep(1)
