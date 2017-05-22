from decimal import Decimal as D

import factory
import factory.django

from core import models

LIST_NAME = ['Edgar', 'Estefania', 'Gvame', 'Ivan', 'Miguel', 'Xurxo', 'Yago']
LIST_SURNAME = ['Alcántara', 'Benítez', 'Fernández', 'González', 'Nieto', 'Orge', 'Souto']


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group
    group_name = factory.Sequence(lambda n: "Group %02d" % n)


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Person
    name = factory.Iterator(LIST_NAME)
    surname = factory.Iterator(LIST_SURNAME)


class RecipientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Recipient
    category = 'child'
    person = factory.SubFactory(PersonFactory)


class VolunteerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Volunteer
    comment = 'Example comment'
    person = factory.SubFactory(PersonFactory)


class CustodianFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Custodian
    category = 'legal'
    person = factory.SubFactory(PersonFactory)
    minor = factory.SubFactory(RecipientFactory)


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Membership
    membership_fee = D('15.00')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Member
    person = factory.SubFactory(PersonFactory)
    membership = factory.SubFactory(MembershipFactory)
