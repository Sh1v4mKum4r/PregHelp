from datetime import datetime
from typing import Dict, Any


class HealthStats:
def __init__(self, blood_pressure: float, sugar_level: float, weight: float, timestamp: datetime):
self.blood_pressure = blood_pressure
self.sugar_level = sugar_level
self.weight = weight
self.date_time = timestamp
self.is_manual = True


def record_manual(self) -> None:
self.is_manual = True


def record_automatic(self) -> None:
self.is_manual = False


def view_stats(self) -> Dict[str, Any]:
return {
"blood_pressure": self.blood_pressure,
"sugar_level": self.sugar_level,
"weight": self.weight,
"date_time": self.date_time.isoformat(),
"is_manual": self.is_manual,
}