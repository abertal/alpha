from django.shortcuts import render

from core import models


def group_list(request):
    object_list = models.Group.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/main.html', context=context)


def group_detail(request, pk):
    obj = models.Group.objects.get(pk=pk)
    people = models.Person.objects.filter(enrolment__group=obj)
    context = {'object': obj, 'people': people}
    return render(request, 'webapp/detail.html', context=context)


def person_list(request):
    object_list = models.Person.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/person_list.html', context=context)


def person_detail(request, pk):
    object = models.Person.objects.get(pk=pk)
    context = {'object': object}
    return render(request, 'webapp/person_detail.html', context=context)


def missing_doc(request):
    pending = models.PersonMembership.objects.exclude(id_card_status='si')
    object_list = models.Membership.objects.filter(personmembership__in=pending).distinct()
    context = {'object_list': object_list}
    return render(request, 'webapp/missing_doc.html', context=context)
