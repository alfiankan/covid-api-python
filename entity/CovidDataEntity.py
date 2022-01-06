from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TotalCase:
    total_positive: int = 0
    total_hospitalized: int = 0
    total_recovered: int = 0
    total_dead: int = 0
    new_positive: int = 0
    new_hospitalized: int = 0
    new_recovered: int = 0
    new_dead: int = 0
