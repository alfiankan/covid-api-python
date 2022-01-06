from json.decoder import JSONDecodeError
from typing import Any
import requests
from entity.CovidDataEntity import TotalCase

class CovidDataRepository():
    def __init__(self):
        self.requestTimeOut = 30 #second

    def errorSimulation(self):
        pass

    def getUpdateData(self):
        try:
            r = requests.get('https://data.covid194.go.id/public/api/update.json', timeout=self.requestTimeOut)
            resulData = r.json()["update"]
            # return data, error
            return TotalCase(
                positive= resulData["total"]["jumlah_positif"],
                hospitalized= resulData["total"]["jumlah_dirawat"],
                recovered= resulData["total"]["jumlah_sembuh"],
                dead= resulData["total"]["jumlah_meninggal"],
                newPositive= resulData["penambahan"]["jumlah_positif"],
                newHospitalized= resulData["penambahan"]["jumlah_dirawat"],
                newRecovered= resulData["penambahan"]["jumlah_sembuh"],
                newDead= resulData["penambahan"]["jumlah_meninggal"],
            ), None
        except Exception as e:
            return TotalCase(), e

