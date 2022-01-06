from json.decoder import JSONDecodeError
from typing import Any, List
import requests
from entity.CovidDataEntity import DailyCase, TotalCase
import datetime

class CovidDataRepository():
    """
    Repository class hold data source.

    """
    def __init__(self):
        self._requestTimeOut = 30 #second

    def getDailyCases(self):
        """get source data public api
                returns:
                    (DailyCases): result daily cases data
        """
        try:
            # start request to source api
            r = requests.get('https://data.covid19.go.id/public/api/update.json', timeout=self._requestTimeOut)
            resultData = r.json()['update']["harian"]

            # create daily list object
            dailyData:List[DailyCase] = list()
            for row in resultData:
                dailyData.append(DailyCase(
                    date=row['key']/1000,
                    positive=row['jumlah_positif']['value'],
                    recovered=row['jumlah_sembuh']['value'],
                    death=row['jumlah_meninggal']['value'],
                    active=row['jumlah_positif']['value']
                ))

            return dailyData, None
        except Exception as e:
            # catch error
            return [], e


    def getLastUpdateSummary(self):
        """get source data from public api
                returns:
                    (TotalCase): result summary cases data
        """
        try:
            # start request to source api
            r = requests.get('https://data.covid19.go.id/public/api/update.json', timeout=self._requestTimeOut)
            resultData = r.json()['update']
            # return data, error
            return TotalCase(
                total_positive= resultData['total']['jumlah_positif'],
                total_active= resultData['total']['jumlah_dirawat'],
                total_recovered= resultData['total']['jumlah_sembuh'],
                total_death= resultData['total']['jumlah_meninggal'],
                new_positive= resultData['penambahan']['jumlah_positif'],
                new_active= resultData['penambahan']['jumlah_dirawat'],
                new_recovered= resultData['penambahan']['jumlah_sembuh'],
                new_death= resultData['penambahan']['jumlah_meninggal'],
            ), None
        except Exception as e:
            # catch error
            return TotalCase(), e

