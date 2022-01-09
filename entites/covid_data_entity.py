from dataclasses import dataclass, asdict
from typing import Any
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TotalCase:
    """Represent Total Covid Case"""
    total_positive: int = 0
    total_recovered: int = 0
    total_deaths: int = 0
    total_active: int = 0
    new_positive: int = 0
    new_recovered: int = 0
    new_deaths: int = 0
    new_active: int = 0

@dataclass_json
@dataclass
class DailyCase:
    """Represent DailyCase Covid Case"""
    date: Any = 0
    positive: int = 0
    recovered: int = 0
    deaths: int = 0
    active: int = 0


@dataclass_json
@dataclass
class YearlyCase:
    """Represent YearlyCase Covid Case"""
    year: Any = 0
    positive: int = 0
    recovered: int = 0
    deaths: int = 0
    active: int = 0



@dataclass_json
@dataclass
class MonthlyCase:
    """Represent MonthlyCase Covid Case"""
    month: Any = 0
    positive: int = 0
    recovered: int = 0
    deaths: int = 0
    active: int = 0
