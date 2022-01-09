
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

def testTime():
    s = "2020.02"
    res = time.mktime(datetime.strptime(s, "%Y.%m").timetuple())
    print(res)
    print(datetime.utcfromtimestamp(res).strftime("%Y.%m"))

    print("NOW {}".format(time.time()))
    print("add month",datetime.strptime("2020.01", "%Y.%m") + relativedelta(months=9))
    print(datetime.utcfromtimestamp(time.time()).strftime("%Y.%m"))

