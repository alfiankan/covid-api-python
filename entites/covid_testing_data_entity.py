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
