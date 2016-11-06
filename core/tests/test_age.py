import datetime as dt
from core import models


def test_age_eighteen_year():
    birthday = dt.date.today()
    birthday = birthday.replace(year=birthday.year - 18)
    person = models.Person(birthday=birthday)
    assert person.age == '18 años'
