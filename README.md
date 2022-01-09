[![Build & Test](https://github.com/alfiankan/covid-api-python/actions/workflows/python-app.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/python-app.yml)  &nbsp;&nbsp; [![Docker Hub Image](https://github.com/alfiankan/covid-api-python/actions/workflows/build-image.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/build-image.yml) &nbsp;&nbsp; [![Deploy to Heroku.](https://github.com/alfiankan/covid-api-python/actions/workflows/heroku.yml/badge.svg)](https://github.com/alfiankan/covid-api-python/actions/workflows/heroku.yml)

# Indonesia Covid-19 Api

## Table of Content
- [ How to use ](#1)
- [ Requirements ](#2)
- [ How to build ](#3)
- [ How to test ](#4)
- [ How to run ](#5)
- [ Architectural Design ](#6)
- [ Src ](#7)
- [ Data Integrity ](#8)
- [ Docker Image ](#9)
- [ Api Docs ](#10)

<a name="1"></a>
## How to use
  1. Using Deployed App
     > You can use : https://indonesia-covid-api.herokuapp.com
  2. Build from source
     > Follow this step : [ How to build ](#3)
  3. Using prebuilt Docker image
      ```
      docker container run -p 3000:3000 alfiantech/indonesia-covid-api:lastest
      ```

<a name="2"></a>
## Requirements 
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
  6. To run production server run `export PORT=3000 && make start`
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
  - To run production server run `make start`
      > output
      ```
      ╰─ export PORT=3000 && make start
        python3 sync_scheduler.py & export FLASK_ENV=production && gunicorn --bind 0.0.0.0:3000 api:app --access-logfile logs/access.log --capture-output
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Starting gunicorn 20.1.0
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Listening at: http://0.0.0.0:3000 (31407)
        [2022-01-09 15:25:08 +0700] [31407] [INFO] Using worker: sync
        [2022-01-09 15:25:08 +0700] [31408] [INFO] Booting worker with pid: 31408
      ```
  - To run as docker container `docker container run -p 3000:3000 alfiantech/indonesia-covid-api:lastest`

<a name="6"></a>
## Architectural Design

<a name="7"></a>
## Src

<a name="8"></a>
## Data Integrity

<a name="9"></a>
## Docker Image

<a name="10"></a>
## Api Docs







## Todo :
<a name="desc"></a>

- [x] Entry point for all API, provide general information of covid cases.
- [x] Provide yearly data of total covid cases.
- [x] Provide yearly data of total covid cases of the year provided in <year>.

- [x] Provide monthly data of total covid cases.
- [x] Provide monthly data of total covid cases in the year provided in <year>.
- [x] Provide monthly data of total covid cases in the month and year provided in <year> and <month>.

- [x] Provide daily data of covid cases.
- [x] Provide daily data of covid cases in the year provided in <year>
- [x] Provide daily data of covid cases in the year and month provided in <year> and <month>
- [x] Provide daily data of covid cases on the day provided in <year>, <month> and, <date>





- [x] Entry point for all API, provide general information of vaccination.
- [x] Provide yearly data of total vaccination.
- [x] Provide yearly data of total vaccination of the year provided in <year>.

- [x] Provide monthly data of total vaccination.
- [x] Provide monthly data of total vaccination in the year provided in <year>.
- [x] Provide monthly data of total vaccination in the month and year provided in <year> and <month>.

- [x] Provide daily data of vaccination.
- [x] Provide daily data of vaccination in the year provided in <year>
- [x] Provide daily data of vaccination in the year and month provided in <year> and <month>.
- [x] Provide daily data of vaccination on the day provided in <year>, <month> and, <date>.



[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e?action=collection%2Ffork&collection-url=entityId%3D7847165-0d3be7de-dd45-4183-822c-174b6ef6db3e%26entityType%3Dcollection%26workspaceId%3D04cc5d73-b93a-4a0e-ae83-43e1c6e73e6d#?env%5Bnodeflux%5D=W3sia2V5IjoiaG9zdCIsInZhbHVlIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIiwiZW5hYmxlZCI6dHJ1ZX1d)
