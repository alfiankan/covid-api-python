from dataclasses import dataclass, asdict
from typing import Any
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DailyCovidTestData:
    date: Any = 0
    pcr_tcm_specimen: int = 0
    antigen_specimen: int = 0
    antigen: int = 0
    pcr_tcm: int = 0


@dataclass_json
@dataclass
class TotalCovidTestData():
    total_pcr_tcm_specimen: int = 0
    total_antigen_specimen: int = 0
    total_antigen: int = 0
    total_pcr_tcm: int = 0

    new_pcr_tcm_specimen: int = 0
    new_antigen_specimen: int = 0
    new_antigen: int = 0
    new_pcr_tcm: int = 0


@dataclass_json
@dataclass
class YearlyCovidTestData():
    year: Any = 0
    pcr_tcm_specimen: int = 0
    antigen_specimen: int = 0
    antigen: int = 0
    pcr_tcm: int = 0


@dataclass_json
@dataclass
class MonthlyCovidTestData():
    month: Any = 0
    pcr_tcm_specimen: int = 0
    antigen_specimen: int = 0
    antigen: int = 0
    pcr_tcm: int = 0
