import logging
from typing import List
import requests
from entites.covid_data_entity import DailyCase
from entites.covid_testing_data_entity import DailyCovidTestData
from entites.vaccination_data_entity import DailyVaccinationData

class MinistryDataRepository():
    """
    Repository class hold data source.
    From https://data.covid19.go.id

    """
    def __init__(self):
        # request connection timeout
        self._requestTimeOut = 30 #second
        self.logger = logging.getLogger('root')

    def getDailyTestAndVaccinationData(self):
        """get source data public api
                returns:
                    (List[DailyCase]): result daily vaccination and test data
        """
        try:
            # start request to source api
            r = requests.get('https://data.covid19.go.id/public/api/pemeriksaan-vaksinasi.json', timeout=self._requestTimeOut)

            # get vacc data
            resultVacData = r.json()['vaksinasi']["harian"]

            # create daily vacc list object
            dailyVaccData: List[DailyVaccinationData] = list()
            for row in resultVacData:
                dailyVaccData.append(DailyVaccinationData(
                    date=row['key']/1000,
                    first_vacc=row['jumlah_vaksinasi_1']['value'],
                    second_vacc=row['jumlah_vaksinasi_2']['value'],
                ))

            # get covid test data
            resultCovidTestData = r.json()['pemeriksaan']["harian"]

            # create daily vacc list object
            dailyCovidTestData: List[DailyCovidTestData] = list()
            for row in resultCovidTestData:
                dailyCovidTestData.append(DailyCovidTestData(
                    date=row['key']/1000,
                    pcr_tcm=row['jumlah_orang_pcr_tcm']['value'],
                    antigen=row['jumlah_orang_antigen']['value'],
                    pcr_tcm_specimen=row['jumlah_spesimen_pcr_tcm']['value'],
                    antigen_specimen=row['jumlah_spesimen_antigen']['value'],
                ))

            return dailyVaccData, dailyCovidTestData, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], [], e



    def getDailyCases(self):
        """get source data public api
                returns:
                    (List[DailyCase]): result daily cases data
        """
        try:
            # start request to source api
            r = requests.get('https://data.covid19.go.id/public/api/update.json', timeout=self._requestTimeOut)
            resultData = r.json()['update']["harian"]

            # create daily list object
            dailyData: List[DailyCase] = list()
            for row in resultData:
                dailyData.append(DailyCase(
                    date=row['key']/1000,
                    positive=row['jumlah_positif']['value'],
                    recovered=row['jumlah_sembuh']['value'],
                    deaths=row['jumlah_meninggal']['value'],
                    active=row['jumlah_positif']['value']
                ))

            return dailyData, None

        except Exception as e:
            # catch error
            self.logger.error(e)
            return [], e
