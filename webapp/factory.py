import factory

from core import models


def aleatory_name():
    names = ['Miguel', 'Iván N', 'Iván S', 'Yago', 'Edgar']
    surnames = ['migonzalvar', 'ivannieto', 'isGroba', 'benitezdemiguel', 'Alcántara']
    return factory.Iterator(names), factory.Iterator(surnames)


class PersonFactory(factory.Factory):
    class Meta:
        model = models.Person
    name, surname = aleatory_name()


class VolunteerFactory(factory.Factory):
    class Meta:
        model = models.Volunteer
    person = factory.SubFactory(PersonFactory)
    comment = factory.Sequence(lambda n: 'Comment%d' % n)


class GroupFactory(factory.Factory):
    class Meta:
        model = models.Group
    group_name = factory.Sequence(lambda n: 'Example_group%d' % n)


class EventFactory(factory.Factory):
    class Meta:
        model = models.Event
    event_name = factory.Sequence(lambda n: 'Example_event%d' % n)
    event_start = '23/03/2017'
    event_end = '24/04/2017'
    comment = factory.Sequence(lambda n: 'Comment%d' % n)


class RecipientFactory(factory.Factory):
    class Meta:
        model = models.Recipient
    person = factory.SubFactory(PersonFactory)
    category = 'child'


class CustodianFactory(factory.Factory):
    class Meta:
        model = models.Custodian
    category = 'mother'
    person = factory.SubFactory(PersonFactory)
    minor = factory.SubFactory(RecipientFactory)
