from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class FilterConfig:
    start_date: datetime
    end_date: datetime
    global_average: float
    selected_stations: List[str]
    selected_sensor: str
    human_readable_sensor: str
    target_year: int
