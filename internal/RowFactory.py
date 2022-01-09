from entites.covid_data_entity import DailyCase, TotalCase, YearlyCase, MonthlyCase
from entites.vaccination_data_entity import DailyVaccinationData, MonthlyVaccinationData, TotalVaccinationData, YearlyVaccinationData
from entites.covid_testing_data_entity import DailyCovidTestData, MonthlyCovidTestData, TotalCovidTestData, YearlyCovidTestData

class RowFactory():

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
                    total_deaths=row[2],
                    total_active=row[3],
                    new_positive=row[4],
                    new_recovered=row[5],
                    new_deaths=row[6],
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
                    deaths=row[3],
                    active=row[4]
                )

    def MonthlyCaseRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to MonthlyCase class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (MonthlyCase): MonthlyCase class object
        """
        return MonthlyCase(
                    month=row[0],
                    positive=row[1],
                    recovered=row[2],
                    deaths=row[3],
                    active=row[4]
                )

    def DailyCaseRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to MonthlyCase class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (DailyCase): MonthlyCase class object
        """
        return DailyCase(
                    date=row[0],
                    positive=row[1],
                    recovered=row[2],
                    deaths=row[3],
                    active=row[4]
                )

    def TotalVaccinationRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to TotalVaccination class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (Total): TotalVaccination class object
        """
        return TotalVaccinationData(
                    total_first_vacc=row[0],
                    total_second_vacc=row[1],
                    new_first_vacc=row[2],
                    new_second_vacc=row[3]
                )

    def YearlyVaccinationRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to YearlyVaccination class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (DailyCase): YearlyVaccination class object
        """
        return YearlyVaccinationData(
                    year=row[0],
                    first_vacc=row[1],
                    second_vacc=row[2]
                )

    def MonthlyVaccinationRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to YearlyVaccination class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (MonthlyVaccinationData): YearlyVaccination class object
        """
        return MonthlyVaccinationData(
                    month=row[0],
                    first_vacc=row[1],
                    second_vacc=row[2]
                )

    def DailyVaccinationRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to DailyVaccinationData class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (DailyVaccinationData): DailyVaccinationData class object
        """
        return DailyVaccinationData(
                    date=row[0],
                    first_vacc=row[1],
                    second_vacc=row[2]
                )


    def TotalCovidTestDataRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to TotalCovidTestData class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (TotalCovidTestData): TotalCovidTestData class object
        """
        return TotalCovidTestData(
                    total_pcr_tcm_specimen = row[0],
                    total_antigen_specimen = row[1],
                    total_antigen = row[2],
                    total_pcr_tcm = row[3],
                    new_pcr_tcm_specimen = row[4],
                    new_antigen_specimen = row[5],
                    new_antigen = row[6],
                    new_pcr_tcm = row[7]
                )

    def YearlyCovidTestDataRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to YearlyCovidTestData class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (YearlyCovidTestData): YearlyCovidTestData class object
        """
        return YearlyCovidTestData(
                    year = row[0],
                    pcr_tcm_specimen = row[1],
                    antigen_specimen = row[2],
                    antigen = row[3],
                    pcr_tcm = row[4]
                )

    def MonthlyCovidTestDataRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to YearlyVaccination class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (YearlyVaccination): YearlyVaccination class object
        """
        return MonthlyCovidTestData(
                    month = row[0],
                    pcr_tcm_specimen = row[1],
                    antigen_specimen = row[2],
                    antigen = row[3],
                    pcr_tcm = row[4]
                )

    def DailyCovidTestDataRowFactory(self, cursor, row):
        """
        Sqlite row factory transfrom query result to DailyCovidTestData class object

                Parameters:
                        cursor (sqlite3.Cursor): sqlite cursor
                        row : row result tuple

                Returns:
                        (DailyCovidTestData): DailyCovidTestData class object
        """
        return DailyCovidTestData(
                    date = row[0],
                    pcr_tcm_specimen = row[1],
                    antigen_specimen = row[2],
                    antigen = row[3],
                    pcr_tcm = row[4]
                )
