from django.shortcuts import render

from core import models


def group_list(request):
    object_list = models.Group.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/main.html', context=context)

def group_detail(request, pk):
    object = models.Group.objects.get(pk=pk)
    context = {'object': object}
    return render(request, 'webapp/detail.html', context=context)


def person_list(request):
    object_list = models.Person.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/person_list.html', context=context)

def person_detail(request, pk):
    object = model.Person.objects.get(pk=pk)
    context = {'object': object}
    return render(request, 'webapp/person_detail.html', context=context)