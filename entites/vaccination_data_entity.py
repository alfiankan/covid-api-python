from dataclasses import dataclass
from typing import Any
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DailyVaccinationData:
    date: Any = 0
    first_vacc: int = 0
    second_vacc: int = 0


@dataclass_json
@dataclass
class TotalVaccinationData():
    total_first_vacc: int = 0
    total_second_vacc: int = 0
    new_first_vacc: int = 0
    new_second_vacc: int = 0


@dataclass_json
@dataclass
class YearlyVaccinationData():
    year: Any = 0
    first_vacc: int = 0
    second_vacc: int = 0


@dataclass_json
@dataclass
class MonthlyVaccinationData():
    month: Any = 0
    first_vacc: int = 0
    second_vacc: int = 0
