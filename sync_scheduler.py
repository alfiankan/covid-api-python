from repositories.CovidDataRepository import CovidDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
from sqlalchemy import engine as alchemyEngine
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql import text
import schedule
import logging
import time

from usecases.CovidUseCase import CovidUseCase

# DATABASE SYNC SCHEDULER ENTRY POINT
# create db object
db = alchemyEngine.create_engine('sqlite:///covid_database.db', poolclass=StaticPool)

def runSync():
    repo = CovidDataRepository(db.connect())
    ministryRepo = MinistryDataRepository()
    app = CovidUseCase(repo, ministryRepo)
    err = app.syncDataWithApiSource()
    if err == None:
        print("Sync Success...")
    else:
        print(err)

runSync()
schedule.every(5).hours.do(runSync)
while True:
  schedule.run_pending()
  time.sleep(1)
