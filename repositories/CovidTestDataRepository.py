import logging
import sqlite3
from typing import List
from pypika import Query
from entites.covid_testing_data_entity import DailyCovidTestData, MonthlyCovidTestData, TotalCovidTestData, YearlyCovidTestData
from internal.RowFactory import RowFactory


class CovidTestDataRepository():
    """
    Repository class hold data covid test.

    Attributes
    ----------
    db : sqlite3.Connection
        database connection object
    """
    def __init__(self, db: sqlite3.Connection):
        self._db = db
        self._tableName = 'test'
        self._rowFactory = RowFactory()
        self.logger = logging.getLogger('root')

    def getLastUpdateSummary(self):
        """
        get last updated data, latest covid test in date, and total all data

                Returns:
                        (Total): last updated data, and total
                        (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        SUM(pcr_tcm_specimen),
                        SUM(antigen_specimen),
                        SUM(antigen),
                        SUM(pcr_tcm),
                        (SELECT pcr_tcm_specimen FROM {0} ORDER BY key DESC LIMIT 1),
                        (SELECT antigen_specimen FROM {0} ORDER BY key DESC LIMIT 1),
                        (SELECT antigen FROM {0} ORDER BY key DESC LIMIT 1),
                        (SELECT pcr_tcm FROM {0} ORDER BY key DESC LIMIT 1)
                        FROM {0}""".format(self._tableName)

            self._db.row_factory = self._rowFactory.TotalCovidTestDataRowFactory
            result: TotalCovidTestData = self._db.cursor().execute(stmt).fetchone()
            return result, None

        except Exception as e:
            self.logger.error(e)
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
            self.logger.error(e)
            return e

    def bulkInsertDailyData(self, data: List[DailyCovidTestData]):
        """
        bulk Inserting covid test data

                Parameters:
                        data (DailyCovidTestData]): dailys data

                Returns:
                        (error): sqlite error query return None if has no error
        """
        try:
            # build query statement for bulk insert
            stmt = Query.Table(self._tableName)
            for row in data:
                stmt = stmt.insert((row.date, row.pcr_tcm_specimen, row.antigen_specimen, row.antigen, row.pcr_tcm))

            #  insert
            self._db.execute(str(stmt))
            return None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return e

    def getYearlyData(self, since: int, upto: int):
        """
        get data  yearly, with filter ability (since, upto), default is returning all yearly data

                Parameters:
                        since (int): filter year start
                        upto (int): filter year end

                Returns:
                         (List[Yearlycovid testData]): yearly list result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(pcr_tcm_specimen),
                        SUM(antigen_specimen),
                        SUM(antigen),
                        SUM(pcr_tcm)
                        FROM {}
                        WHERE CAST(year as desimal) BETWEEN ? AND ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyCovidTestDataRowFactory
            result = self._db.cursor().execute(stmt, (since, upto))

            dbResult: List[YearlyCovidTestData] = list(result)
            return dbResult, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], e

    def getDataByYear(self, year: int):
        """
        gets data by year,

                Parameters:
                        year (int): year

                Returns:
                         (YearlyCovidTestData): yearly result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y',datetime(key, 'unixepoch')) AS year,
                        SUM(pcr_tcm_specimen),
                        SUM(antigen_specimen),
                        SUM(antigen),
                        SUM(pcr_tcm)
                        FROM {}
                        WHERE CAST(year as desimal) = ?
                        GROUP BY year""".format(self._tableName)

            self._db.row_factory = self._rowFactory.YearlyCovidTestDataRowFactory
            result: YearlyCovidTestData = self._db.cursor().execute(stmt, (year,)).fetchone()

            return result, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], e

    def getMonthlyData(self, since: float, upto: float):
        """
        gets data monthly
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (MonthlyCovidTestData): Monthlycovid testData result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m',datetime(key, 'unixepoch')) AS month,
                        SUM(pcr_tcm_specimen),
                        SUM(antigen_specimen),
                        SUM(antigen),
                        SUM(pcr_tcm)
                        FROM {}
                        WHERE key BETWEEN ? AND ?
                        GROUP BY month""".format(self._tableName)

            self._db.row_factory = self._rowFactory.MonthlyCovidTestDataRowFactory
            result: list[MonthlyCovidTestData] = list(self._db.cursor().execute(stmt, (since, upto,)))

            return result, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], e

    def getDailyData(self, since: float, upto: float):
        """
        gets data daily
                Parameters:
                        since (timestamp unix): filter  start
                        upto (timestamp unix): filter  end
                Returns:
                         (DailyCovidTestDataRowFactory): MonthlyData result
                         (error): query error return None if has no error
        """
        try:
            stmt = """SELECT
                        strftime('%Y-%m-%d',datetime(key, 'unixepoch')) AS date,
                        pcr_tcm_specimen,
                        antigen_specimen,
                        antigen,
                        pcr_tcm
                        FROM {}""".format(self._tableName)

            self._db.row_factory = self._rowFactory.DailyCovidTestDataRowFactory
            result: list[DailyCovidTestData] = list(self._db.cursor().execute(stmt))

            return result, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], e
