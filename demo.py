"""
demo.py — Demonstration script for the Smart Pregnancy & Health Monitoring System

This script imports the domain model from `healthcare_models.py` (assumed to be in the same
folder) and runs a sequence of demonstrations covering:
 - User management
 - Vaccination schedule
 - Health tracking
 - Reminders
 - Appointment booking
 - AI ChatBot
 - SOS emergency alert
 - Health alerts
 - Doctor dashboard
 - Appointment management
 - Emergency response (assigning task)
 - Prescription -> reminder creation

Usage:
    python demo.py

If `healthcare_models.py` is not present, the script will inform you and exit.
"""

from datetime import datetime, date, timedelta
import sys

try:
    import healthcare_models as hm
except Exception as e:
    print("ERROR: failed to import healthcare_models.py. Make sure it exists in the same folder.")
    print("Import error:", e)
    sys.exit(1)

print("\\n=== Smart Pregnancy & Health Monitoring System — Demo ===\n")

# -----------------------------
# 1. User Management
# -----------------------------
print("Demonstrating User Management:")
user = hm.User(person_id=1, name="Alice Smith", age=30, contact=1234567890, gender="F", user_id=101, password="secure_pass")
print(f"User created: {user.name}, ID: {user.user_id}")

# Update profile
user.update_profile(age=31, contact=9876543210)
print(f"User profile updated. New age: {user.age}, New contact: {user.contact}")

# Login
ok = user.login("secure_pass")
print(f"Login success: {ok}\n")

# -----------------------------
# 2. Vaccination Schedule
# -----------------------------
print("Demonstrating Vaccination Schedule:")
baby_dob = date(2023, 1, 15)
due_date = date(2024, 2, 1)
vacc = hm.Vaccination(vaccine_id=1, baby_dob=baby_dob, vaccine_name="MMR Dose 1", due_date=due_date)
schedule = vacc.generate_schedule()
print("Generated schedule (sample entries):")
for s in schedule:
    print(" -", s)
reminder_sent = vacc.send_reminder()
print("Reminder within 3 days triggered:", reminder_sent)
vacc.confirm_completion()
print(f"Vaccination status: {vacc.status}\n")

# -----------------------------
# 3. Health Tracking
# -----------------------------
print("Demonstrating Health Tracking:")
hs1 = hm.HealthStats(blood_pressure=120.5, sugar_level=95.0, weight=65.2, timestamp=datetime(2024,1,10,8,0,0))
hs2 = hm.HealthStats(blood_pressure=125.0, sugar_level=102.5, weight=65.5, timestamp=datetime(2024,1,11,8,30,0))
hs3 = hm.HealthStats(blood_pressure=118.0, sugar_level=98.0, weight=65.0, timestamp=datetime(2024,1,12,9,0,0))
user.add_health_stats(hs1)
user.add_health_stats(hs2)
user.add_health_stats(hs3)
print("User health stats:")
for hs in user.view_health_status():
    print(" -", hs)
print()

# -----------------------------
# 4. Reminders
# -----------------------------
print("Demonstrating Reminders:")
rem_time = datetime.now() - timedelta(minutes=1)  # scheduled slightly in the past for demo
rem = hm.Reminder(reminder_id=1, name="Iron Supplement", schedule_time=rem_time, dosage=10.0)
user.reminders.append(rem)
print(f"Created reminder {rem.medicine_name} scheduled at {rem.schedule_time}")
was_sent = rem.send_notification()
print("send_notification() returned:", was_sent, "status:", rem.status)
rem.mark_taken()
print("After mark_taken():", rem.status, "\n")

# -----------------------------
# 5. Appointment Booking
# -----------------------------
print("Demonstrating Appointment Booking:")
doc = hm.Doctor(person_id=2, name="Dr. House", age=50, contact=9988776655, gender="M", doctor_id=201, password="doc_pass", specialization="Diagnostics")
appt_time = datetime.now() + timedelta(days=2)
appt = hm.Appointment(appointment_id=1001, user=user, doctor=doc, date_time=appt_time)
user.book_appointment(appt)
print("Booked appointment:", {"id": appt.appointment_id, "user": appt.user.name, "doctor": appt.doctor.name, "date_time": appt.date_time, "status": appt.status})
print()

# -----------------------------
# 6. AI ChatBot
# -----------------------------
print("Demonstrating AI ChatBot:")
bot = hm.ChatBot()
print("Q: Hello ->", bot.process_query("Hello"))
print("Q: What is normal bp? ->", bot.process_query("what is normal bp"))
print()

# -----------------------------
# 7. SOS Emergency Alert
# -----------------------------
print("Demonstrating SOS Emergency Alert:")
user.add_sos_contact("Partner", "+447120001234")
sos = user.trigger_sos(location="51.5074N,0.1278W", health_snapshot="BP:140/95, Sugar:180")
print("SOS created with id:", sos.sos_id)
if user.assigned_doctor:
    print("Assigned doctor appointments after SOS:", [a.appointment_id for a in user.assigned_doctor.appointments])
print()

# -----------------------------
# 8. Health Alerts (threshold detection)
# -----------------------------
print("Demonstrating Health Alerts:")
# add a critical stat
crit = hm.HealthStats(blood_pressure=180.0, sugar_level=100.0, weight=66.0, timestamp=datetime(2024,1,13,10,0,0))
user.add_health_stats(crit)

# simple detector
alerts = []
for hs in user.health_stats:
    if hs.blood_pressure >= 160 or hs.sugar_level >= 250:
        alerts.append(("critical", hs))
    elif hs.blood_pressure >= 140 or hs.sugar_level >= 180:
        alerts.append(("warning", hs))

print("Detected alerts:")
for level, hs in alerts:
    print(f" - {level.upper()}: BP={hs.blood_pressure}, Sugar={hs.sugar_level}, Time={hs.date_time}")
print()

# -----------------------------
# 9. Doctor Dashboard
# -----------------------------
print("Demonstrating Doctor Dashboard:")
# perform login with doctor's password
logged_in = doc.login("doc_pass")
print(f"Doctor {doc.name} logged in: {logged_in}")
print(f"Doctor viewing health stats for {user.name}:")
for s in doc.view_patient_stats(user):
    print(" -", s)
print("Doctor managing appointments (summaries):")
print(doc.manage_appointments())
print()

# -----------------------------
# 10. Appointment Management (Confirm + Reschedule)
# -----------------------------
print("Demonstrating Appointment Management (Doctor):")
appt.confirm_appointment()
print("After confirm -> status:", appt.status)
new_time = datetime.now() + timedelta(days=5)
appt.reschedule(new_time)
print("After reschedule -> status:", appt.status, ", new time:", appt.date_time)
print()

# -----------------------------
# 11. Emergency Response (Doctor -> Assistant)
# -----------------------------
print("Demonstrating Emergency Response (Doctor assigning task):")
assistant = hm.Assistant(person_id=3, name="Nurse Jane", age=25, contact=1122334455, gender="F", assistant_id=301)
doc.assign_task(assistant, "Prepare emergency room for critical patient and notify ICU team.")
print("Assistant current task:", assistant.current_task)
print()

# -----------------------------
# 12. Prescription Management -> Reminder creation
# -----------------------------
print("Demonstrating Prescription -> Reminder creation:")
med_name = "Folic Acid"
dosage = 0.4
instructions = "Take one tablet daily with food."
print(f"Doctor {doc.name} prescribes {med_name} {dosage}mg to {user.name}")
# create reminder for next day 8 AM
reminder_time = datetime.now() + timedelta(days=1)
reminder_time = reminder_time.replace(hour=8, minute=0, second=0, microsecond=0)
pres_rem = hm.Reminder(reminder_id=2, name=med_name, schedule_time=reminder_time, dosage=dosage)
user.reminders.append(pres_rem)
print("Created prescription reminder for", user.name, "at", pres_rem.schedule_time)

print("\\n=== Demo complete ===")
