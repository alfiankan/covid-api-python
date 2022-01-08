from json.decoder import JSONDecodeError
import sqlite3
from typing import List
from pypika import Query
from entites.covid_data_entity import DailyCase, MonthlyCase, TotalCase, YearlyCase
import datetime

from entites.RowFactory import RowFactory

class CovidDataRepository():
    """
    Repository class hold data source.

    Attributes
    ----------
    db : sqlite3.Connection
        database connection object
    """
    def __init__(self, db: sqlite3.Connection):
        self._db = db
        self._tableName = 'covid_cases'
        self._rowFactory = RowFactory()


    def getLastUpdateSummary(self):
        """
        get last updated data, latest covid case in date, and total all data

                Returns:
                        (TotalCase): last updated data, and total cases
                        (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        SUM(positive),
                        SUM(recovered),
                        SUM(death),
                        SUM(active),
                        (SELECT positive FROM covid_cases ORDER BY key DESC LIMIT 1),
                        (SELECT recovered FROM covid_cases ORDER BY key DESC LIMIT 1),
                        (SELECT death FROM covid_cases ORDER BY key DESC LIMIT 1),
                        (SELECT active FROM covid_cases ORDER BY key DESC LIMIT 1)
                        FROM {}""".format(self._tableName)

            self._db.row_factory = self._rowFactory.TotalCaseRowFactory
            result: TotalCase = self._db.cursor().execute(stmt).fetchone()
            return result, None

        except Exception as e:
            return None, e


    def truncateData(self):
        """
        set empty database data by deleting all record

                Returns:
                        (error): sqlite query error
        """
        try:
            # empty database
            stmt = "DELETE FROM {}".format(self._tableName)
            self._db.execute(stmt)
            return None

        except Exception as e:
            # catch error
            return e


    def bulkInsertDailyCaseData(self, data: List[DailyCase]):
        """
        bulk Inserting covid case data

                Parameters:
                        data (ListDailyCase]): daily cases data

                Returns:
                        (error): sqlite error query return None if has no error
        """
        try:
            # build query statement for bulk insert
            stmt = Query.Table(self._tableName)
            for row in data:
                stmt = stmt.insert((row.date, row.positive, row.recovered, row.death, row.active))

            #  insert
            self._db.execute(str(stmt))
            return None
            
        except Exception as e:
            # catch error
            return e



    def getYearlyCases(self, since: int, upto: int):
        """
        get data  yearly, with filter ability (since, upto), default is returning all yearly data

                Parameters:
                        since (int): filter year start
                        upto (int): filter year end

                Returns:
                         (List[YearlyCase]): yearly case list result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(positive),
                        SUM(recovered),
                        SUM(death),
                        SUM(active)
                        FROM {}
                        WHERE CAST(year as desimal) BETWEEN ? AND ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyCaseRowFactory
            result = self._db.cursor().execute(stmt, (since, upto))

            dbResult: List[YearlyCase] = list(result)
            return dbResult, None

        except Exception as e:
            # catch error
            return [], e


    def getCaseByYear(self, year: int):
        """
        get cases data by year,

                Parameters:
                        year (int): year

                Returns:
                         (YearlyCase): yearly case result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(positive),
                        SUM(recovered),
                        SUM(death),
                        SUM(active)
                        FROM {}
                        WHERE CAST(year as desimal) = ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyCaseRowFactory
            result: YearlyCase = self._db.cursor().execute(stmt, (year,)).fetchone()

            return result, None

        except Exception as e:
            # catch error
            return [], e


    def getMonthlyData(self, since: float, upto: float):
        """
        get cases data monthly
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (MonthlyCase): MonthlyCase case result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m',datetime(key, 'unixepoch')) AS month,
                        SUM(positive),
                        SUM(recovered),
                        SUM(death),
                        SUM(active)
                        FROM {}
                        WHERE key BETWEEN ? AND ?
                        GROUP BY month""".format(self._tableName)

            self._db.row_factory = self._rowFactory.MonthlyCaseRowFactory
            result: list[MonthlyCase] = list(self._db.cursor().execute(stmt, (since, upto,)))

            return result, None

        except Exception as e:
            # catch error
            return [], e


    def getDailyData(self, since: float, upto: float):
        """
        get cases data daily
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (DailyCase): MonthlyCase case result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m-%d',datetime(key, 'unixepoch')) AS date,
                        positive,
                        recovered,
                        death,
                        active
                        FROM {}
                        WHERE key BETWEEN ? AND ?""".format(self._tableName)

            self._db.row_factory = self._rowFactory.DailyCaseRowFactory
            result: list[DailyCase] = list(self._db.cursor().execute(stmt, (since, upto,)))

            return result, None

        except Exception as e:
            # catch error
            return [], e
