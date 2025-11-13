from datetime import datetime
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
from .user import User
from .doctor import Doctor


class Appointment:
def __init__(self, appointment_id: int, user: Optional['User'], doctor: Optional['Doctor'], date_time: datetime):
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