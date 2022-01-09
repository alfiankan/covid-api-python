[![Build & Test](https://github.com/alfiankan/covid-api-python/actions/workflows/python-app.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/python-app.yml)  &nbsp;&nbsp; [![Docker Hub Image](https://github.com/alfiankan/covid-api-python/actions/workflows/build-image.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/build-image.yml) &nbsp;&nbsp; [![Deploy to Heroku.](https://github.com/alfiankan/covid-api-python/actions/workflows/heroku.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/heroku.yml)

# Indonesia Covid-19 Api

## Table of Content
- [ How to use ](#1)
- [ Requirements ](#2)
- [ How to build ](#3)
- [ How to test ](#4)
- [ How to run ](#5)
- [ Architectural Design ](#6)
- [ Scheduler ](#7)
- [ Notes ](#8)
- [ Data Integrity ](#9)
- [ Docker Image ](#10)
- [ Api Docs ](#11)

<a name="1"></a>
## How to use
  1. Using Deployed App<br>
     > You can use : https://indonesia-covid-api.herokuapp.com <br><br>
     > [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e?action=collection%2Ffork&collection-url=entityId%3D7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e%26entityType%3Dcollection%26workspaceId%3D04cc5d73-b93a-4a0e-ae83-43e1c6e73e6d#?env%5Bnodeflux%5D=W3sia2V5IjoiaG9zdCIsInZhbHVlIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIiwiZW5hYmxlZCI6dHJ1ZX1d)
  2. Build from source
     > Follow this step : [ How to build ](#3)
  3. Using prebuilt Docker image
      ```
      docker container run -p <HOST_PORT>:3000 alfiantech/indonesia-covid-api:lastest
      ```

<a name="2"></a>
## Requirements 
  - python 3
  - make
  - install python required package using : 
    ```
    make install
    ```

<a name="3"></a>
## How to build &nbsp;&nbsp;🔨
  1. Make sure all requirements already installed
  2. To install predefined python package use `make install`
  4. To sync with source data run `make syncdata`
  5. To run development server run `make dev`
  6. To run production server run `export PORT=<HOST_PORT> && make start`
  7. To build as docker image run `docker build -t <imagename>:<tag> .`


<a name="4"></a>
## How to test &nbsp;&nbsp; 🧪
  - Verbose testing run `make test`
      > output :
      
        tests/unit/database_test.py::testSqliteConnection PASSED                                          [ 88%]
        tests/unit/ministry_repository_test.py::testGetDailyCaseData PASSED                               [ 89%]
        tests/unit/ministry_repository_test.py::testGetDailyVaccinationData PASSED                        [ 91%]
        tests/unit/playground_test.py::testTime PASSED                                                    [ 92%]
        tests/unit/validator_test.py::testIsTypeValid PASSED                                              [ 93%]
        tests/unit/validator_test.py::testIsEmpty PASSED                                                  [ 94%]
        tests/unit/validator_test.py::testValidateIsNumber PASSED                                         [ 96%]
        tests/unit/validator_test.py::testValidationErrMessage PASSED                                     [ 97%]
        tests/unit/validator_test.py::testIsValidationError PASSED                                        [ 98%]
        tests/unit/validator_test.py::testValidateDateInput PASSED                                        [100%]
        
  - Coverage test run `make cover`
      > Output :
      
                  ---------- coverage: platform darwin, python 3.9.7-final-0 -----------
        Name                                                                                Stmts   Miss  Cover
        -------------------------------------------------------------------------------------------------------
        /Users/alfiankan/Library/Python/3.9/lib/python/site-packages/greenlet/__init__.py      19      2    89%
        api.py                                                                                 30      2    93%
        entites/BaseEntity.py                                                                   9      0   100%
        entites/__init__.py                                                                     0      0   100%
        entites/covid_data_entity.py                                                           38      0   100%
        entites/covid_testing_data_entity.py                                                   11      0   100%
        entites/vaccination_data_entity.py                                                     26      0   100%
        handlers/CovidApiHandler.py                                                           178     48    73%
        handlers/VaccinationApiHandler.py                                                     178     38    79%
        handlers/__init__.py                                                                    0      0   100%
        internal/RowFactory.py                                                                 19      0   100%
        internal/__init__.py                                                                    0      0   100%
        repositories/CovidDataRepository.py                                                    76     18    76%
        repositories/MinistryDataRepository.py                                                 36      6    83%
        repositories/VaccinationDataRepository.py                                              76     18    76%
        repositories/__init__.py                                                                0      0   100%
        tests/__init__.py                                                                       0      0   100%
        tests/integration/__init__.py                                                           0      0   100%
        tests/integration/covid_api_handler_test.py                                           200     16    92%
        tests/integration/covid_repository_test.py                                             66      0   100%
        tests/integration/covid_usecase_test.py                                                37      0   100%
        tests/integration/vaccination_api_handler_test.py                                     197      0   100%
        tests/integration/vaccination_repository_test.py                                       65      0   100%
        tests/integration/vaccination_usecase_test.py                                          37      0   100%
        tests/unit/__init__.py                                                                  0      0   100%
        tests/unit/database_test.py                                                             4      0   100%
        tests/unit/ministry_repository_test.py                                                 21      0   100%
        tests/unit/playground_test.py                                                          11      0   100%
        tests/unit/validator_test.py                                                           25      0   100%
        usecases/CovidUseCase.py                                                               43     11    74%
        usecases/VaccinationUseCase.py                                                         42     11    74%
        validation/__init__.py                                                                  0      0   100%
        validation/http_api_validation.py                                                      29      2    93%
        -------------------------------------------------------------------------------------------------------
        TOTAL                                                                                1473    172    88%


        ========================================== 78 passed in 3.98s ===========================================

<a name="5"></a>
## How to run &nbsp;&nbsp; ⚙️
  - To run development server run `make dev`
        > output
      ```
      ╰─ make dev
      export FLASK_ENV=development && python3 api.py
      * Serving Flask app 'api' (lazy loading)
      * Environment: development
      * Debug mode: on
      werkzeug - INFO -  * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
      werkzeug - INFO -  * Restarting with stat
      werkzeug - WARNING -  * Debugger is active!
      werkzeug - INFO -  * Debugger PIN: 639-723-256
      ```
  - To run production server run `export PORT=<HOST_PORT> && make start`
      > output
      ```
      ╰─ export PORT=3000 && make start
        python3 sync_scheduler.py & export FLASK_ENV=production && gunicorn --bind 0.0.0.0:3000 api:app --access-logfile logs/access.log --capture-output
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Starting gunicorn 20.1.0
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Listening at: http://0.0.0.0:3000 (31407)
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Using worker: sync
        [2022-01-09 15:25:08 +0700] [31408] [INFO] Booting worker with pid: 31408
      ```
  - To run as docker container `docker container run -p <HOST_PORT>:3000 alfiantech/indonesia-covid-api:lastest`

<a name="6"></a>
## Architectural Design
![arch](https://user-images.githubusercontent.com/40946917/148677969-2517fd9b-cd3b-487d-9c41-9211e96a03d9.jpeg)

  - this application adopts a clean architecture design with some modification. the main layer is repository, usecase, and handler
  - folder :
      - entity folder contains data class object, represents data which will be processed in the application
      - repository folder contains class that handles the process of querying data from the database and requests to the public api, the repository aims to interact directly with the data and then convert it to entity object
      - usecase folder contains usecase/business logic as interfaces to (app api) that can be used by various handlers such as http api, cli, rpc, etc.
      - handler folder contains class to handle requests from users, in this case via the http api, the handler will validate and adjust the request so that it can be used to run the use case. returned data from use case will be sent again to the user.
      - internal folder contains library/module

<a name="7"></a>
## scheduler
   ![sync](https://user-images.githubusercontent.com/40946917/148677976-7e1a5c57-9845-4c6b-a48d-a4690a424f4e.jpeg)

  - scheduler run sync job every 1 hours
  - scheduler will terminate if main app down, using health checking
  - the app is not to directly make an api call to the public api https://data.covid19.go.id/public/api/ because :
      - https://data.covid19.go.id/public/api/ api is not realtime, from my research is update +1, for example: today data will be shown tommorow. 
      - if we make a request directly to the public api (user -> app -> public api) will increase latency or my be egress bandwidth, or other things like public api server being spiked (become slow).
      - by syncing for x intervals and storing as local data (or it can be called cache) will provide other benefits like we can use sql script to run data agregation or filtering.

<a name="8"></a>
## Note
    - 

<a name="9"></a>
## Data Integrity
  - to make sure local data is up to date, scheduler will doing this job every 1 hour

<a name="10"></a>
## Docker Image
    https://hub.docker.com/r/alfiantech/indonesia-covid-api

<a name="11"></a>
## Api Docs
  > here is API docs with example response :<br><br>
  [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e?action=collection%2Ffork&collection-url=entityId%3D7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e%26entityType%3Dcollection%26workspaceId%3D04cc5d73-b93a-4a0e-ae83-43e1c6e73e6d#?env%5Bnodeflux%5D=W3sia2V5IjoiaG9zdCIsInZhbHVlIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIiwiZW5hYmxlZCI6dHJ1ZX1d)







