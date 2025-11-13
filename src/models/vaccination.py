from datetime import date, timedelta
from typing import List, Dict, Any


class Vaccination:
def __init__(self, vaccine_id:int, baby_dob:date, vaccine_name:str, due_date:date):
self.vaccine_id = vaccine_id
self.baby_dob = baby_dob
self.vaccine_name = vaccine_name
self.due_date = due_date
self.status = "pending"


def generate_schedule(self) -> List[Dict[str, Any]]:
offsets = [0, 6*7, 10*7, 14*7, 9*30, 15*30]
schedule = []
for i, days in enumerate(offsets):
due = self.baby_dob + timedelta(days=days)
status = "pending" if due >= date.today() else "overdue"
schedule.append({"dose_number": i+1, "vaccine_name": self.vaccine_name, "due_date": due.isoformat(), "status": status})
return schedule


def send_reminder(self) -> bool:
from datetime import date
today = date.today()
days_until = (self.due_date - today).days
if 0 <= days_until <= 3 and self.status == "pending":
return True
return False


def confirm_completion(self) -> None:
self.status = "completed"