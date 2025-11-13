from typing import List, Optional
from .person import Person
from .health_stats import HealthStats
from .reminder import Reminder
from .appointment import Appointment
from .sos import SOS
import hashlib


def _hash_password(p: str) -> str:
return hashlib.sha256(p.encode("utf-8")).hexdigest()


class User(Person):
def __init__(self, person_id:int, name:str, age:int, contact:int, gender:str, user_id:int, password:str):
super().__init__(person_id, name, age, contact, gender)
self.user_id = user_id
self.password_hash = _hash_password(password)
self.health_stats: List[HealthStats] = []
self.reminders: List[Reminder] = []
self.appointments: List[Appointment] = []
self.sos_contacts = []
self.assigned_doctor: Optional['Doctor'] = None


def login(self, password: str) -> bool:
return self.password_hash == _hash_password(password)


def add_health_stats(self, stats: HealthStats) -> None:
self.health_stats.append(stats)


def view_health_status(self):
return [hs.view_stats() for hs in self.health_stats]


def add_sos_contact(self, name:str, phone:str) -> None:
self.sos_contacts.append({"name":name, "phone":phone})


def trigger_sos(self, location:str, health_snapshot:str) -> SOS:
from itertools import count
sos_id = next(count(1000))
sos = SOS(sos_id, self, location, health_snapshot)
sos.send_alert()
return sos