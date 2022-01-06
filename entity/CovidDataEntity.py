from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TotalCase:
    positive: int = 0
    hospitalized: int = 0
    recovered: int = 0
    dead: int = 0
    newPositive: int = 0
    newHospitalized: int = 0
    newRecovered: int = 0
    newDead: int = 0
