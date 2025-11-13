from __future__ import annotations
from typing import List, Dict, Optional, Any
from datetime import date, datetime, timedelta
import hashlib
import itertools

# Simple ID generator for entities that don't have DB-backed IDs
_id_counter = itertools.count(1)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Person:
    def __init__(self, person_id: int, name: str, age: int, contact: int, gender: str):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.contact = contact
        self.gender = gender

    def update_profile(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def view_profile(self) -> Dict[str, Any]:
        return {
            "person_id": self.person_id,
            "name": self.name,
            "age": self.age,
            "contact": self.contact,
            "gender": self.gender,
        }


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


class Reminder:
    def __init__(self, reminder_id: int, name: str, schedule_time: datetime, dosage: float = 0):
        self.reminder_id = reminder_id
        self.medicine_name = name
        self.dosage = dosage
        self.schedule_time = schedule_time
        self.status = "pending"

    def set_reminder(self, new_time: Optional[datetime] = None, new_dosage: Optional[float] = None) -> None:
        if new_time:
            self.schedule_time = new_time
            self.status = "pending"
        if new_dosage is not None:
            self.dosage = new_dosage

    def send_notification(self) -> bool:
        now = datetime.now()
        if self.status == "pending" and now >= self.schedule_time:
            self.status = "sent"
            # In a real app we'd push notification. Here we return True to indicate sent.
            return True
        return False

    def mark_taken(self) -> None:
        self.status = "taken"


class Appointment:
    def __init__(self, appointment_id: int, user: User | None, doctor: Doctor | None, date_time: datetime):
        self.appointment_id = appointment_id
        self.user = user
        self.doctor = doctor
        self.date_time = date_time
        self.status = "booked"

    def book_appointment(self) -> None:
        self.status = "booked"
        if self.user and self not in self.user.appointments:
            self.user.appointments.append(self)
        if self.doctor and self not in self.doctor.appointments:
            self.doctor.appointments.append(self)

    def confirm_appointment(self) -> None:
        self.status = "confirmed"

    def reschedule(self, new_time: datetime) -> None:
        self.date_time = new_time
        self.status = "rescheduled"

    def cancel(self) -> None:
        self.status = "cancelled"


class User(Person):
    def __init__(
        self,
        person_id: int,
        name: str,
        age: int,
        contact: int,
        gender: str,
        user_id: int,
        password: str,
    ):
        super().__init__(person_id, name, age, contact, gender)
        self.user_id = user_id
        self.password_hash = _hash_password(password)
        self.health_stats: List[HealthStats] = []
        self.reminders: List[Reminder] = []
        self.appointments: List[Appointment] = []
        self.sos_contacts: List[Dict[str, str]] = []
        self.assigned_doctor: Optional[Doctor] = None

    def login(self, password: str) -> bool:
        return self.password_hash == _hash_password(password)

    def update_profile(self, **kwargs) -> None:
        super().update_profile(**kwargs)

    def view_health_status(self) -> List[Dict[str, Any]]:
        return [hs.view_stats() for hs in self.health_stats]

    def add_health_stats(self, stats: HealthStats) -> None:
        self.health_stats.append(stats)

    def book_appointment(self, appointment: Appointment) -> None:
        appointment.user = self
        appointment.book_appointment()

    def trigger_sos(self, location: str, health_snapshot: str) -> SOS:
        sos_id = next(_id_counter)
        sos = SOS(sos_id, self, location, health_snapshot)
        sos.send_alert()
        return sos

    def add_sos_contact(self, name: str, phone: str) -> None:
        self.sos_contacts.append({"name": name, "phone": phone})


class Doctor(Person):
    def __init__(
        self,
        person_id: int,
        name: str,
        age: int,
        contact: int,
        gender: str,
        doctor_id: int,
        password: str,
        specialization: str,
    ):
        super().__init__(person_id, name, age, contact, gender)
        self.doctor_id = doctor_id
        self.password_hash = _hash_password(password)
        self.specialization = specialization
        self.patients: List[User] = []
        self.appointments: List[Appointment] = []

    def login(self, password: str) -> bool:
        return self.password_hash == _hash_password(password)

    def view_patient_stats(self, user: User) -> List[Dict[str, Any]]:
        return user.view_health_status()

    def manage_appointments(self) -> List[Dict[str, Any]]:
        return [
            {
                "appointment_id": appt.appointment_id,
                "user": appt.user.name if appt.user else None,
                "date_time": appt.date_time.isoformat(),
                "status": appt.status,
            }
            for appt in sorted(self.appointments, key=lambda x: x.date_time)
        ]

    def assign_task(self, assistant: Assistant, task: str) -> None:
        assistant.update_task(task)

    def add_patient(self, user: User) -> None:
        if user not in self.patients:
            self.patients.append(user)
            user.assigned_doctor = self


class SOS:
    def __init__(self, sos_id: int, user: User, location: str, health_snapshot: str):
        self.sos_id = sos_id
        self.user = user
        self.location = location
        self.health_snapshot = health_snapshot
        self.timestamp = datetime.now()

    def send_alert(self) -> None:
        # Notify doctor if assigned, notify emergency contacts
        self.notify_doctor()
        self.notify_contacts()
        # In a real system we'd persist the SOS and send external notifications.

    def notify_doctor(self) -> None:
        doc = self.user.assigned_doctor
        if doc:
            # For this stub, we'll add a quick "alert appointment" to doctor's queue
            alert_appt = Appointment(next(_id_counter), self.user, doc, datetime.now())
            alert_appt.status = "sos-alert"
            doc.appointments.append(alert_appt)

    def notify_contacts(self) -> None:
        for contact in self.user.sos_contacts:
            # In real app we'd send SMS/call; here we simulate by printing to console (or no-op)
            pass


class Vaccination:
    def __init__(self, vaccine_id: int, baby_dob: date, vaccine_name: str, due_date: date):
        self.vaccine_id = vaccine_id
        self.baby_dob = baby_dob
        self.vaccine_name = vaccine_name
        self.due_date = due_date
        self.status = "pending"

    def generate_schedule(self) -> List[Dict[str, Any]]:
        # Basic illustrative schedule (days after DOB): birth, 6w, 10w, 14w, 9m, 15m
        offsets = [0, 6 * 7, 10 * 7, 14 * 7, 9 * 30, 15 * 30]  # days (approx for months)
        schedule = []
        for i, days in enumerate(offsets):
            due = self.baby_dob + timedelta(days=days)
            schedule.append(
                {
                    "dose_number": i + 1,
                    "vaccine_name": self.vaccine_name,
                    "due_date": due.isoformat(),
                    "status": "pending" if due >= date.today() else "overdue" if due < date.today() else "pending",
                }
            )
        return schedule

    def send_reminder(self) -> bool:
        # Simulate a reminder if due_date is within 3 days
        today = date.today()
        days_until = (self.due_date - today).days
        if 0 <= days_until <= 3 and self.status == "pending":
            return True
        return False

    def confirm_completion(self) -> None:
        self.status = "completed"


class ChatBot:
    def __init__(self):
        self.knowledge_base: Dict[str, str] = {
            "what is a normal bp": "Normal blood pressure is generally around 120/80 mmHg.",
            "when to call a doctor": "If you experience severe pain, heavy bleeding, fever, or trouble breathing, contact your doctor immediately.",
        }

    def process_query(self, query: str) -> str:
        return self.respond(query)

    def respond(self, query: str) -> str:
        q = query.strip().lower()
        if "hello" in q or "hi" in q:
            return "Hello! How can I help you today?"
        # exact match first
        if q in self.knowledge_base:
            return self.knowledge_base[q]
        # simple keyword search
        for k, v in self.knowledge_base.items():
            if k in q or any(word in q for word in k.split()):
                return v
        return "I'm not sure about that. Please consult your healthcare provider."

    def add_knowledge(self, question: str, answer: str) -> None:
        self.knowledge_base[question.strip().lower()] = answer.strip()


class HospitalManagement:
    def __init__(self, hospital_id: int, name: str, contact_info: int):
        self.hospital_id = hospital_id
        self.name = name
        self.contact_info = contact_info
        self.doctors: List[Doctor] = []
        self.appointments: List[Appointment] = []

    def manage_doctors(self) -> List[Dict[str, Any]]:
        return [{"doctor_id": d.doctor_id, "name": d.name, "specialization": d.specialization} for d in self.doctors]

    def add_doctor(self, doctor: Doctor) -> None:
        if doctor not in self.doctors:
            self.doctors.append(doctor)

    def remove_doctor(self, doctor: Doctor) -> None:
        if doctor in self.doctors:
            self.doctors.remove(doctor)

    def manage_appointments(self) -> List[Dict[str, Any]]:
        # Aggregate appointments across doctors
        appts = []
        for d in self.doctors:
            for a in d.appointments:
                appts.append(
                    {
                        "appointment_id": a.appointment_id,
                        "doctor": d.name,
                        "user": a.user.name if a.user else None,
                        "date_time": a.date_time.isoformat(),
                        "status": a.status,
                    }
                )
        # sort by date_time
        appts.sort(key=lambda x: x["date_time"])
        return appts


class Nurse(Person):
    def __init__(self, person_id: int, name: str, age: int, contact: int, gender: str, nurse_id: int):
        super().__init__(person_id, name, age, contact, gender)
        self.nurse_id = nurse_id
        self.current_task = ""

    def update_care_task(self, task: str) -> None:
        self.current_task = task


class Assistant(Person):
    def __init__(self, person_id: int, name: str, age: int, contact: int, gender: str, assistant_id: int):
        super().__init__(person_id, name, age, contact, gender)
        self.assistant_id = assistant_id
        self.current_task = ""

    def update_task(self, task: str) -> None:
        self.current_task = task
