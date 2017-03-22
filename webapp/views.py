from django.shortcuts import redirect, render, reverse
from django.views import generic

from core import models

from . import forms


class Option:
    def __init__(self, name, viewname, args=None, kwargs=None, menu=None):
        self.name = name
        self.url = reverse(viewname, args, kwargs) if viewname else False
        self.menu = menu

    def is_current(self):
        return self.menu.current == self.name


class MenuBar:
    def __init__(self, current):
        self.current = current

    def get_options(self):
        return [
            Option('Personas', 'person-list', menu=self),
            Option('Detalle persona', None, menu=self),
            Option('Detalle destinatario', None, menu=self),
            Option('Detalle Voluntario', None, menu=self),
            Option('Socios', 'membership-list', menu=self),
            Option('Detalle socio', None, menu=self),
            Option('Nuevo socio individual', 'basicformnewperson', menu=self),
            Option('Nueva familia', 'basicformnewfamily', menu=self),
        ]

    def __iter__(self):
        return iter(self.get_options())


def group_list(request):
    object_list = models.Group.objects.all()
    context = {'object_list': object_list}
    return render(request, 'webapp/main.html', context=context)


def group_detail(request, pk):
    obj = models.Group.objects.get(pk=pk)
    people = models.Person.objects.filter(enrolment__group=obj)
    context = {'object': obj, 'people': people}
    return render(request, 'webapp/detail.html', context=context)


def missing_doc(request):
    pending = models.Member.objects.exclude(id_card_status='si')
    object_list = models.Membership.objects.filter(member__in=pending).distinct()
    context = {'object_list': object_list}
    return render(request, 'webapp/missing_doc.html', context=context)


def login(request):
    context = {}
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'webapp/login.html', context=context)


class MenuMixin:
    name = ''

    def get_context_data(self, **kwargs):
        if 'menu' not in kwargs:
            kwargs['menu'] = MenuBar(self.name)
        return super().get_context_data(**kwargs)


class Home(MenuMixin, generic.TemplateView):
    name = 'Inicio'
    template_name = 'webapp/home.html'


class NewIndividualMember(MenuMixin, generic.FormView):
    form_class = forms.NewIndividualMember
    template_name = 'webapp/basicformnewperson.html'
    name = 'Nuevo socio individual'

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class NewFamilyMember(MenuMixin, generic.FormView):
    form_class = forms.NewFamilyMember
    template_name = 'webapp/basicformnewfamily.html'
    name = 'Nueva familia'

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class PersonList(MenuMixin, generic.ListView):
    template_name = 'webapp/person_list.html'
    name = 'Personas'

    def get_queryset(self):
        return models.Person.objects.all()


class PersonDetail(MenuMixin, generic.DetailView):
    model = models.Person
    template_name = 'webapp/person_detail.html'
    name = 'Detalle persona'


class PersonEdit(MenuMixin, generic.UpdateView):
    model = models.Person
    form_class = forms.EditPerson
    template_name = 'webapp/person_edit.html'
    name = 'Detalle persona'

    def get_success_url(self):
        return reverse('person-detail', args=[self.object.id])


class RecipientDetail(MenuMixin, generic.DetailView):
    model = models.Recipient
    template_name = 'webapp/recipient_detail.html'
    name = 'Detalle destinatario'


class RecipientEdit(MenuMixin, generic.UpdateView):
    model = models.Recipient
    form_class = forms.RecipientEdit
    template_name = 'webapp/recipient_edit.html'
    name = 'Detalle destinatario'

    def get_success_url(self):
        return reverse('recipient-detail', args=[self.object.id])


class VolunteerEdit(MenuMixin, generic.DetailView):
    model = models.Volunteer
    form_class = forms.VolunteerEdit
    template_name = 'webapp/volunteer_edit.html'
    name = 'Detalle voluntario'


class VolunteerDetail(MenuMixin, generic.DetailView):
    model = models.Volunteer
    template_name = 'webapp/volunteer_detail.html'
    name = 'Detalle voluntario'

    def get_success_url(self):
        return reverse('volunteer-detail', args=[self.object.id])


class MembershipList(MenuMixin, generic.ListView):
    template_name = 'webapp/membership_list.html'
    name = 'Socios'

    def get_queryset(self):
        return models.Membership.objects.all()


class MembershipDetail(MenuMixin, generic.DetailView):
    model = models.Membership
    template_name = 'webapp/membership_detail.html'
    name = 'Detalle socio'
