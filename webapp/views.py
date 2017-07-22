from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.views import generic

from django_filters.views import FilterView

from core import models

from . import filters, forms


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
            Option(_('Personas'), 'person-list', menu=self),
            Option(_('Detalle persona'), None, menu=self),
            Option(_('Destinatarios'), 'recipient-list', menu=self),
            Option(_('Detalle destinatario'), None, menu=self),
            Option(_('Voluntarios'), 'volunteer-list', menu=self),
            Option(_('Detalle voluntario'), None, menu=self),
            Option(_('Membresías'), 'membership-list', menu=self),
            Option(_('Socios'), 'member-list', menu=self),
            Option(_('Detalle socio'), None, menu=self),
            Option(_('Grupos'), 'group-list', menu=self),
            Option(_('Detalle grupo'), None, menu=self),
            Option(_('Proyectos'), 'project-list', menu=self),
            Option(_('Detalle proyecto'), None, menu=self),
            Option(_('Actividades'), 'event-list', menu=self),
            Option(_('Detalle actividad'), None, menu=self),
            Option(_('Nuevo socio individual'), 'basicformnewperson', menu=self),
            Option(_('Nueva familia'), 'basicformnewfamily', menu=self),
        ]

    def __iter__(self):
        return iter(self.get_options())


def missing_doc(request):
    pending = models.Member.objects.exclude(id_card_status='si')
    object_list = models.Membership.objects.filter(
        member__in=pending).distinct()
    context = {'object_list': object_list}
    return render(request, 'webapp/missing_doc.html', context=context)


class Login(LoginView):
    template_name = 'webapp/login.html'
    redirect_authenticated_user = 'home'


class Logout(LogoutView):
    pass


class MenuMixin:
    name = ''

    def get_context_data(self, **kwargs):
        if 'menu' not in kwargs:
            kwargs['menu'] = MenuBar(self.name)
        return super().get_context_data(**kwargs)


class FromPersonMixin:
    def get_person(self):
        id_ = self.kwargs['pk']
        return models.Person.objects.get(id=id_)

    def get_initial(self):
        person = self.get_person()
        return {'person': person.id}

    def get_context_data(self, **kwargs):
        kwargs['person'] = self.get_person()
        return super().get_context_data(**kwargs)


class Home(LoginRequiredMixin, MenuMixin, generic.TemplateView):
    template_name = 'webapp/home.html'
    name = ugettext_lazy('Página principal')


class NewIndividualMember(LoginRequiredMixin, MenuMixin, generic.FormView):
    form_class = forms.NewIndividualMember
    template_name = 'webapp/basicformnewperson.html'
    name = ugettext_lazy('Nuevo socio individual')

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class NewFamilyMember(LoginRequiredMixin, MenuMixin, generic.FormView):
    form_class = forms.NewFamilyMember
    template_name = 'webapp/basicformnewfamily.html'
    name = ugettext_lazy('Nueva familia')

    def form_valid(self, form):
        membership = form.execute()
        return redirect('membership-detail', pk=membership.pk)


class PersonList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/person/list.html'
    name = ugettext_lazy('Personas')
    model = models.Person
    filterset_class = filters.PersonFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Person.objects.order_by('-id')


class PersonDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Person
    template_name = 'webapp/person/detail.html'
    name = ugettext_lazy('Detalle persona')


class PersonCreate(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.CreateView):
    model = models.Person
    form_class = forms.CreatePerson
    template_name = 'webapp/person/create.html'
    success_message = ugettext_lazy('Persona creada correctamente')
    name = ugettext_lazy('Crear persona')

    def get_success_url(self):
        return reverse('person-detail', args=[self.object.id])


class PersonEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Person
    form_class = forms.EditPerson
    template_name = 'webapp/person/edit.html'
    name = ugettext_lazy('Detalle persona')
    success_message = ugettext_lazy('Persona editada correctamente')

    def get_success_url(self):
        return reverse('person-detail', args=[self.object.id])


class PersonDelete(LoginRequiredMixin, MenuMixin, generic.DeleteView):
    model = models.Person
    template_name = 'webapp/person/delete.html'
    name = ugettext_lazy('Eliminar persona')
    success_url = reverse_lazy('person-list')
    success_message = ugettext_lazy('Persona eliminada correctamente')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
        except ProtectedError:
            self.success_message = ugettext_lazy('Persona no eliminada')
            messages.error(self.request, self.success_message)
        response = HttpResponseRedirect(success_url)
        return response


class RecipientCreate(LoginRequiredMixin, SuccessMessageMixin,
                      MenuMixin, FromPersonMixin, generic.CreateView):
    model = models.Recipient
    form_class = forms.RecipientCreate
    template_name = 'webapp/recipient/create.html'
    success_message = ugettext_lazy('Destinatario creado correctamente')
    name = ugettext_lazy('Crear destinatario')

    def get_success_url(self):
        return reverse('recipient-detail', args=[self.object.id])


class RecipientDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Recipient
    template_name = 'webapp/recipient/detail.html'
    name = ugettext_lazy('Detalle destinatario')


class RecipientEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Recipient
    form_class = forms.RecipientEdit
    template_name = 'webapp/recipient/edit.html'
    name = ugettext_lazy('Detalle destinatario')
    success_message = ugettext_lazy('Destinatario editado correctamente')

    def get_success_url(self):
        return reverse('recipient-detail', args=[self.object.id])


class RecipientList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/recipient/list.html'
    name = ugettext_lazy('Destinatarios')
    model = models.Recipient
    filterset_class = filters.FromPersonFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Recipient.objects.select_related('person').order_by('-id')


class RecipientDelete(LoginRequiredMixin, MenuMixin, generic.DeleteView):
    model = models.Recipient
    template_name = 'webapp/recipient/delete.html'
    name = ugettext_lazy('Eliminar destinatario')
    success_url = reverse_lazy('recipient-list')


class VolunteerCreate(LoginRequiredMixin, SuccessMessageMixin,
                      MenuMixin, FromPersonMixin, generic.CreateView):
    model = models.Volunteer
    form_class = forms.VolunteerCreate
    template_name = 'webapp/volunteer/create.html'
    name = ugettext_lazy('Crear voluntario')
    success_message = ugettext_lazy('Voluntario creado correctamente')
    name = ugettext_lazy('Crear voluntario')

    def get_success_url(self):
        return reverse('volunteer-detail', args=[self.object.id])


class VolunteerEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Volunteer
    form_class = forms.VolunteerEdit
    template_name = 'webapp/volunteer/edit.html'
    name = ugettext_lazy('Detalle voluntario')
    success_message = ugettext_lazy('Voluntario editado correctamente')

    def get_success_url(self):
        return reverse('volunteer-detail', args=[self.object.id])


class VolunteerDetail(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.DetailView):
    model = models.Volunteer
    template_name = 'webapp/volunteer/detail.html'
    name = ugettext_lazy('Detalle voluntario')

    def get_success_url(self):
        return reverse('volunteer-detail', args=[self.object.id])


class VolunteerList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/volunteer/list.html'
    name = ugettext_lazy('Voluntarios')
    model = models.Volunteer
    filterset_class = filters.FromPersonFilter
    paginate_by = 4

    def get_queryset(self):
        return models.Volunteer.objects.select_related('person').order_by('-id')


class VolunteerDelete(LoginRequiredMixin, MenuMixin, generic.DeleteView):
    model = models.Volunteer
    template_name = 'webapp/volunteer/delete.html'
    name = ugettext_lazy('Eliminar voluntario')
    success_url = reverse_lazy('volunteer-list')


class CustodianCreate(LoginRequiredMixin, MenuMixin, generic.CreateView):
    model = models.Custodian
    form_class = forms.CreateCustodian
    template_name = 'webapp/custodian/create.html'
    name = ugettext_lazy('Crea padre, madre, tutor')

    def get_recipient(self):
        id_ = self.kwargs['pk']
        return models.Recipient.objects.get(id=id_)

    def get_initial(self):
        recipient = self.get_recipient()
        return {'minor': recipient.id}

    def get_context_data(self, **kwargs):
        kwargs['recipient'] = self.get_recipient()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('custodian-detail', args=[self.object.id])


class CustodianDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Custodian
    template_name = 'webapp/custodian/detail.html'
    name = ugettext_lazy('Detalle custodian')


class CustodianEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Custodian
    form_class = forms.CustodianEdit
    template_name = 'webapp/custodian/edit.html'
    name = ugettext_lazy('Detalle custodian')

    def get_success_url(self):
        return reverse('custodian-detail', args=[self.object.id])


class EventEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Event
    form_class = forms.EventEdit
    template_name = 'webapp/event/edit.html'
    name = ugettext_lazy('Detalle actividad')

    def get_success_url(self):
        return reverse('event-edit', args=[self.object.id])


class EventCreate(LoginRequiredMixin, MenuMixin, generic.CreateView):
    model = models.Event
    form_class = forms.EventCreate
    template_name = 'webapp/event/create.html'
    name = ugettext_lazy('Nueva actividad')

    def get_success_url(self):
        return reverse('event-edit', args=[self.object.id])


class EventList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/event/list.html'
    name = ugettext_lazy('Actividades')
    filterset_class = filters.EventFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Event.objects.all()


class EventDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Event
    template_name = 'webapp/event/detail.html'
    name = ugettext_lazy('Detalle actividad')

    def get_success_url(self):
        return reverse('event-detail', args=[self.object.id])


class MemberCreate(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, FromPersonMixin, generic.CreateView):
    model = models.Member
    form_class = forms.MemberCreate
    template_name = 'webapp/member/create.html'
    name = ugettext_lazy('Nuevo socio')
    success_message = ugettext_lazy('Socio creado correctamente')

    def get_success_url(self):
        return reverse('member-detail', args=[self.object.id])


class MemberDetail(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.DetailView):
    model = models.Member
    template_name = 'webapp/member/detail.html'
    name = ugettext_lazy('Detalle socio')


class MemberEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Member
    form_class = forms.MemberEdit
    template_name = 'webapp/member/edit.html'
    name = ugettext_lazy('Detalle socio')
    success_message = ugettext_lazy('Socio editado correctamente')

    def get_success_url(self):
        return reverse('member-detail', args=[self.object.id])


class MemberList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/member/list.html'
    name = ugettext_lazy('Socios')
    model = models.Member
    filterset_class = filters.FromPersonFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Member.objects.select_related('person').order_by('-id')


class MembershipList(LoginRequiredMixin, MenuMixin, generic.ListView):
    template_name = 'webapp/membership/list.html'
    name = ugettext_lazy('Membresías')

    def get_queryset(self):
        return models.Membership.objects.all()


class MembershipDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Membership
    template_name = 'webapp/membership/detail.html'
    name = ugettext_lazy('Detalle socio')


class MembershipEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Membership
    form_class = forms.MembershipEdit
    template_name = 'webapp/membership/edit.html'
    name = ugettext_lazy('Detalle socio')

    def get_success_url(self):
        return reverse('membership-detail', args=[self.object.id])


class MembershipCreate(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.CreateView):
    model = models.Membership
    form_class = forms.MembershipCreate
    template_name = 'webapp/membership/create.html'
    name = ugettext_lazy('Creación de membresía')

    def get_person(self):
        id_ = self.kwargs['pk']
        return models.Person.objects.get(id=id_)

    def get_initial(self):
        person = self.get_person()
        return {'person': person.id}

    def get_context_data(self, **kwargs):
        kwargs['person'] = self.get_person()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('membership-detail', args=[self.object.id])


class GroupList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/group/list.html'
    name = ugettext_lazy('Grupos')
    filterset_class = filters.GroupFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Group.objects.all()


class GroupDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Group
    template_name = 'webapp/group/detail.html'
    name = ugettext_lazy('Detalle grupo')


class GroupEdit(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.UpdateView):
    model = models.Group
    form_class = forms.GroupEdit
    template_name = 'webapp/group/edit.html'
    name = ugettext_lazy('Detalle grupo')
    success_message = ugettext_lazy('Grupo editado correctamente')

    def get_success_url(self):
        return reverse('group-detail', args=[self.object.id])


class GroupCreate(LoginRequiredMixin, SuccessMessageMixin, MenuMixin, generic.CreateView):
    model = models.Group
    form_class = forms.GroupCreate
    template_name = 'webapp/group/create.html'
    name = ugettext_lazy('Nuevo grupo')
    success_message = ugettext_lazy('Grupo creado correctamente')

    def get_success_url(self):
        return reverse('group-detail', args=[self.object.id])


class ProjectList(LoginRequiredMixin, MenuMixin, FilterView):
    template_name = 'webapp/project/list.html'
    name = ugettext_lazy('Proyectos')
    filterset_class = filters.ProjectFilter
    paginate_by = 5

    def get_queryset(self):
        return models.Project.objects.all()


class ProjectDetail(LoginRequiredMixin, MenuMixin, generic.DetailView):
    model = models.Project
    template_name = 'webapp/project/detail.html'
    name = ugettext_lazy('Detalle proyecto')


class ProjectEdit(LoginRequiredMixin, MenuMixin, generic.UpdateView):
    model = models.Project
    form_class = forms.ProjectEdit
    template_name = 'webapp/project/edit.html'
    name = ugettext_lazy('Detalle proyecto')

    def get_success_url(self):
        return reverse('project-detail', args=[self.object.id])


class ProjectCreate(LoginRequiredMixin, MenuMixin, generic.CreateView):
    model = models.Project
    form_class = forms.ProjectCreate
    template_name = 'webapp/project/create.html'
    name = ugettext_lazy('Nuevo proyecto')

    def get_success_url(self):
        return reverse('project-detail', args=[self.object.id])


class AjaxPersonList(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        people = models.Person.objects.all()[:10].values('id', 'name')
        return JsonResponse({'data': list(people)})
