import sqlite3
from typing import List
from pypika import Query
from entites.vaccination_data_entity import DailyVaccinationData, MonthlyVaccinationData, TotalVaccinationData, YearlyVaccinationData
from internal.RowFactory import RowFactory


class VaccinationDataRepository():
    """
    Repository class hold data vaccination.

    Attributes
    ----------
    db : sqlite3.Connection
        database connection object
    """
    def __init__(self, db: sqlite3.Connection):
        self._db = db
        self._tableName = 'vaccination'
        self._rowFactory = RowFactory()

    def getLastUpdateSummary(self):
        """
        get last updated data, latest vaccination in date, and total all data

                Returns:
                        (Total): last updated data, and total
                        (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        SUM(first_vacc),
                        SUM(second_vacc),
                        (SELECT first_vacc FROM {0} ORDER BY key DESC LIMIT 1),
                        (SELECT second_vacc FROM {0} ORDER BY key DESC LIMIT 1)
                        FROM {0}""".format(self._tableName)

            self._db.row_factory = self._rowFactory.TotalVaccinationRowFactory
            result: TotalVaccinationData = self._db.cursor().execute(stmt).fetchone()
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

    def bulkInsertDailyData(self, data: List[DailyVaccinationData]):
        """
        bulk Inserting vaccination data

                Parameters:
                        data (ListDailyData]): dailys data

                Returns:
                        (error): sqlite error query return None if has no error
        """
        try:
            # build query statement for bulk insert
            stmt = Query.Table(self._tableName)
            for row in data:
                stmt = stmt.insert((row.date, row.first_vacc, row.second_vacc))

            #  insert
            self._db.execute(str(stmt))
            return None

        except Exception as e:
            # catch error
            return e

    def getYearlyData(self, since: int, upto: int):
        """
        get data  yearly, with filter ability (since, upto), default is returning all yearly data

                Parameters:
                        since (int): filter year start
                        upto (int): filter year end

                Returns:
                         (List[YearlyVaccinationData]): yearly list result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(first_vacc),
                        SUM(second_vacc)
                        FROM {}
                        WHERE CAST(year as desimal) BETWEEN ? AND ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyVaccinationRowFactory
            result = self._db.cursor().execute(stmt, (since, upto))

            dbResult: List[YearlyVaccinationData] = list(result)
            return dbResult, None

        except Exception as e:
            # catch error
            return [], e

    def getDataByYear(self, year: int):
        """
        gets data by year,

                Parameters:
                        year (int): year

                Returns:
                         (YearlyVaccinationData): yearly result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(first_vacc),
                        SUM(second_vacc)
                        FROM {}
                        WHERE CAST(year as desimal) = ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyVaccinationRowFactory
            result: YearlyVaccinationData = self._db.cursor().execute(stmt, (year,)).fetchone()

            return result, None

        except Exception as e:
            # catch error
            return [], e

    def getMonthlyData(self, since: float, upto: float):
        """
        gets data monthly
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (MonthlyVaccinationData): MonthlyVaccinationData result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m',datetime(key, 'unixepoch')) AS month,
                        SUM(first_vacc),
                        SUM(second_vacc)
                        FROM {}
                        WHERE key BETWEEN ? AND ?
                        GROUP BY month""".format(self._tableName)

            self._db.row_factory = self._rowFactory.MonthlyVaccinationRowFactory
            result: list[MonthlyVaccinationData] = list(self._db.cursor().execute(stmt, (since, upto,)))

            return result, None

        except Exception as e:
            # catch error
            return [], e

    def getDailyData(self, since: float, upto: float):
        """
        gets data daily
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (DailyVaccinationData): MonthlyData result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m-%d',datetime(key, 'unixepoch')) AS date,
                        first_vacc,
                        second_vacc
                        FROM {}
                        WHERE key BETWEEN ? AND ?""".format(self._tableName)

            self._db.row_factory = self._rowFactory.DailyVaccinationRowFactory
            result: list[DailyVaccinationData] = list(self._db.cursor().execute(stmt, (since, upto,)))

            return result, None

        except Exception as e:
            # catch error
            return [], e
