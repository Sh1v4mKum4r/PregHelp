from typing import List
from .person import Person
from .appointment import Appointment
import hashlib


def _hash_password(p: str) -> str:
return hashlib.sha256(p.encode("utf-8")).hexdigest()


class Doctor(Person):
def __init__(self, person_id:int, name:str, age:int, contact:int, gender:str, doctor_id:int, password:str, specialization:str):
super().__init__(person_id, name, age, contact, gender)
self.doctor_id = doctor_id
self.password_hash = _hash_password(password)
self.specialization = specialization
self.patients = []
self.appointments: List[Appointment] = []


def login(self, password: str) -> bool:
return self.password_hash == _hash_password(password)


def view_patient_stats(self, user):
return user.view_health_status()


def manage_appointments(self):
return [
{"appointment_id": a.appointment_id, "user": a.user.name if a.user else None, "date_time": a.date_time.isoformat(), "status": a.status}
for a in sorted(self.appointments, key=lambda x: x.date_time)
]


def add_patient(self, user):
if user not in self.patients:
self.patients.append(user)
user.assigned_doctor = self


def assign_task(self, assistant, task: str):
assistant.update_task(task)