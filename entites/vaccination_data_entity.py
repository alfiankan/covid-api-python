from dataclasses import dataclass, asdict
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
    first_vacc: int = 0
    second_vacc: int = 0


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
