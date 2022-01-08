from json.decoder import JSONDecodeError
import sqlite3
from typing import List
from pypika import Query
from entites.CovidDataEntity import DailyCase, TotalCase, YearlyCase
import datetime

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


    def TotalCaseRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to TotalCase class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (TotalCase): TotalCase class object
        """
        return TotalCase(
                    total_positive=row[0],
                    total_recovered=row[1],
                    total_death=row[2],
                    total_active=row[3],
                    new_positive=row[4],
                    new_recovered=row[5],
                    new_death=row[6],
                    new_active=row[7],
                )

    def YearlyCaseRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to YearlyCase class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (YearlyCase): YearlyCase class object
        """
        return YearlyCase(
                    year=row[0],
                    positive=row[1],
                    recovered=row[2],
                    death=row[3],
                    active=row[4]
                )




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

            self._db.row_factory = self.TotalCaseRowFactory
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
        get data by year, with filter ability (since, upto), default is returning all yearly data

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
                        SUM(positive) AS positive,
                        SUM(recovered),
                        SUM(death),
                        SUM(active)
                        FROM {}
                        WHERE CAST(year as desimal) BETWEEN ? AND ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self.YearlyCaseRowFactory
            result = self._db.cursor().execute(stmt, (since, upto))

            dbResult: List[YearlyCase] = list(result)
            return dbResult, None

        except Exception as e:
            # catch error
            return [], e




