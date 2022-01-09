import os
import sqlite3
import argparse
import requests
from repositories.CovidDataRepository import CovidDataRepository
from repositories.MinistryDataRepository import MinistryDataRepository
import schedule
import time
from repositories.VaccinationDataRepository import VaccinationDataRepository
from usecases.CovidUseCase import CovidUseCase
from usecases.VaccinationUseCase import VaccinationUseCase

# DATABASE SYNC SCHEDULER ENTRY POINT
# create db object

def checkMainAppIsRunning():
    """health check
        ping helath check endpoint to make sure scheduler running alongside main app
    """
    time.sleep(10)
    try:
        requests.get('http://localhost:3000/health', timeout=30)
        # ping health app / make sure main app is running
        print('Health ok...')
        return
    except ValueError as e:
        exit()

def runScheduler():
    """run job
        sync local daya with source
    """
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

# args to skip scheduler
skipScheduler = argparse.ArgumentParser(description='Skip long running scheduler')
skipScheduler.add_argument('--skip', action='store_true')
args = skipScheduler.parse_args()

# if skip
if args.skip:
    # run scheduler only once
    runScheduler()
else:
    checkMainAppIsRunning()
    # run job at first time
    runScheduler()
    print('scheduler running on {}'.format(os.getpid()))

    # schedule job every 5 hours
    schedule.every(5).hours.do(runScheduler)
    while True:
        schedule.run_pending()
        time.sleep(1)
