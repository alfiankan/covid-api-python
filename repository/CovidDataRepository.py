from json.decoder import JSONDecodeError
from typing import Any
import requests
from entity.CovidDataEntity import TotalCase

class CovidDataRepository():
    """
    Repository class hold data source.

    """
    def __init__(self):
        self.requestTimeOut = 30 #second

    def errorSimulation(self):
        pass

    def getLastUpdateSummary(self):
        """get source data from https://data.covid19.go.id public api
                returns:
                    (TotalCase): result from api source as data objest
        """
        try:
            # start request to source api
            r = requests.get('https://data.covid19.go.id/public/api/update.json', timeout=self.requestTimeOut)
            resulData = r.json()["update"]
            # return data, error
            return TotalCase(
                total_positive= resulData["total"]["jumlah_positif"],
                total_hospitalized= resulData["total"]["jumlah_dirawat"],
                total_recovered= resulData["total"]["jumlah_sembuh"],
                total_dead= resulData["total"]["jumlah_meninggal"],
                new_positive= resulData["penambahan"]["jumlah_positif"],
                new_hospitalized= resulData["penambahan"]["jumlah_dirawat"],
                new_recovered= resulData["penambahan"]["jumlah_sembuh"],
                new_dead= resulData["penambahan"]["jumlah_meninggal"],
            ), None
        except Exception as e:
            # catch error
            return TotalCase(), e

