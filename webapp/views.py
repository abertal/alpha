from django.shortcuts import render

from core import models


def group_list(request):
    object_list = models.Group.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/main.html', context=context)

#def contact_page(request):
    #return render(request, include('webapp/contact.html'))