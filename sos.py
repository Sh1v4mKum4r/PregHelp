from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
from .user import User


class SOS:
def __init__(self, sos_id: int, user: 'User', location: str, health_snapshot: str):
self.sos_id = sos_id
self.user = user
self.location = location
self.health_snapshot = health_snapshot
self.timestamp = datetime.now()


def send_alert(self) -> None:
# notify doctor (simulate)
if self.user.assigned_doctor:
doc = self.user.assigned_doctor
from .appointment import Appointment
appt = Appointment(9999, self.user, doc, datetime.now())
appt.status = "sos-alert"
doc.appointments.append(appt)
# notify contacts (simulate)
for c in self.user.sos_contacts:
pass