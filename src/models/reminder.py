from datetime import datetime
from typing import Optional


class Reminder:
def __init__(self, reminder_id: int, name: str, schedule_time: datetime, dosage: float = 0.0):
self.reminder_id = reminder_id
self.medicine_name = name
self.dosage = dosage
self.schedule_time = schedule_time
self.status = "pending"


def set_reminder(self, schedule_time: Optional[datetime] = None, dosage: Optional[float] = None) -> None:
if schedule_time:
self.schedule_time = schedule_time
self.status = "pending"
if dosage is not None:
self.dosage = dosage


def send_notification(self) -> bool:
from datetime import datetime
now = datetime.now()
if self.status == "pending" and now >= self.schedule_time:
self.status = "sent"
return True
return False


def mark_taken(self) -> None:
self.status = "taken"