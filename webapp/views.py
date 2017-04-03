from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.views import generic

from django_filters.views import FilterView

from core import models
from webapp.filters import PersonFilter
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
            Option('Detalle voluntario', None, menu=self),
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
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('user'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(
                request,
                'webapp/login.html',
                {'message': 'Por favor introduzca el nombre de usuario'
                    ' y la clave correctos para una cuenta de personal.'})
    else:
        return render(request, 'webapp/login.html', {'message': None})


class MenuMixin:
    name = ''

    def get_context_data(self, **kwargs):
        if 'menu' not in kwargs:
            kwargs['menu'] = MenuBar(self.name)
        return super().get_context_data(**kwargs)


class Home(LoginRequiredMixin, MenuMixin, generic.TemplateView):
    template_name = 'webapp/home.html'


class NewIndividualMember(LoginRequiredMixin, MenuMixin, generic.FormView):
    form_class = forms.NewIndividualMember
    template_name = 'webapp/basicformnewperson.html'
    name = 'Nuevo socio individual'

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class NewFamilyMember(LoginRequiredMixin, MenuMixin, generic.FormView):
    form_class = forms.NewFamilyMember
    template_name = 'webapp/basicformnewfamily.html'
    name = 'Nueva familia'

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class PersonList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/person_list.html'
    name = 'Personas'
    model = models.Person
    filterset_class = PersonFilter

    def get_queryset(self):
        return models.Person.objects.all()


class PersonDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Person
    template_name = 'webapp/person_detail.html'
    name = 'Detalle persona'


class PersonEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Person
    form_class = forms.EditPerson
    template_name = 'webapp/person_edit.html'
    name = 'Detalle persona'

    def get_success_url(self):
        return reverse('person-detail', args=[self.object.id])


class RecipientDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Recipient
    template_name = 'webapp/recipient_detail.html'
    name = 'Detalle destinatario'


class RecipientEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Recipient
    form_class = forms.RecipientEdit
    template_name = 'webapp/recipient_edit.html'
    name = 'Detalle destinatario'

    def get_success_url(self):
        return reverse('recipient-detail', args=[self.object.id])


class VolunteerEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Volunteer
    form_class = forms.VolunteerEdit
    template_name = 'webapp/volunteer_edit.html'
    name = 'Detalle voluntario'


class CustodianDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Custodian
    template_name = 'webapp/custodian_detail.html'
    name = 'Detalle custodian'


class CustodianEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Custodian
    form_class = forms.CustodianEdit
    template_name = 'webapp/custodian_edit.html'
    name = 'Detalle custodian'

    def get_success_url(self):
        return reverse('custodian-detail', args=[self.object.id])


class VolunteerDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Volunteer
    template_name = 'webapp/volunteer_detail.html'
    name = 'Detalle voluntario'

    def get_success_url(self):
        return reverse('volunteer-detail', args=[self.object.id])


class MemberDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Member
    template_name = 'webapp/member_detail.html'
    name = 'Detalle socio'


class MemberEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Member
    form_class = forms.MemberEdit
    template_name = 'webapp/member_edit.html'
    name = 'Detalle socio'

    def get_success_url(self):
        return reverse('member-detail', args=[self.object.id])


class MembershipList(LoginRequiredMixin, MenuMixin, generic.ListView):
    template_name = 'webapp/membership_list.html'
    name = 'Socios'

    def get_queryset(self):
        return models.Membership.objects.all()


class MembershipDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Membership
    template_name = 'webapp/membership_detail.html'
    name = 'Detalle socio'
