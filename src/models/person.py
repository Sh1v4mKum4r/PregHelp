from typing import Any, Dict


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