from typing import List
import requests
from entites.covid_data_entity import DailyCase

class MinistryDataRepository():
    """
    Repository class hold data source.
    From https://data.covid19.go.id

    """
    def __init__(self):
        # request connection timeout
        self._requestTimeOut = 30 #second


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
                    death=row['jumlah_meninggal']['value'],
                    active=row['jumlah_positif']['value']
                ))

            return dailyData, None

        except Exception as e:
            # catch error
            return [], e
