from django.conf.urls import include, url
from django.views.generic import RedirectView

from . import views

person = [
    url(r'^$', views.PersonList.as_view(), name='person-list'),
    url(r'^new/$', views.PersonCreate.as_view(), name='person-create'),
    url(r'^(?P<pk>[^/]+)/$', views.PersonDetail.as_view(), name='person-detail'),
    url(r'^(?P<pk>[^/]+)/edit/$', views.PersonEdit.as_view(), name='person-edit'),
    url(r'^(?P<pk>[^/]+)/volunteer/$', views.VolunteerCreate.as_view(), name='volunteer-create'),
    url(r'^(?P<pk>[^/]+)/recipient/$', views.RecipientCreate.as_view(), name='recipient-create'),
    url(r'^(?P<pk>[^/]+)/member/$', views.MemberCreate.as_view(), name='member-create'),
    url(r'^(?P<pk>[^/]+)/membership/$', views.MembershipCreate.as_view(), name='membership-create'),
]

group = [
    url(r'^(?P<pk>\d+)/edit/$', views.GroupEdit.as_view(), name='group-edit'),
    url(r'^new/$', views.GroupCreate.as_view(), name='group-create'),
]

recipient = [
    url(r'^$', views.RecipientList.as_view(), name='recipient-list'),
    url(r'^(?P<pk>\d+)/$', views.RecipientDetail.as_view(), name='recipient-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.RecipientEdit.as_view(), name='recipient-edit'),
]

volunteer = [
    url(r'^$', views.VolunteerList.as_view(), name='volunteer-list'),
    url(r'^(?P<pk>\d+)/$', views.VolunteerDetail.as_view(), name='volunteer-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.VolunteerEdit.as_view(), name='volunteer-edit'),
]

member = [
    url(r'^$', views.MemberList.as_view(), name='member-list'),
    url(r'^(?P<pk>\d+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.MemberEdit.as_view(), name='member-edit'),
]

custodian = [
    url(r'^(?P<pk>\d+)/$', views.CustodianDetail.as_view(), name='custodian-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.CustodianEdit.as_view(), name='custodian-edit'),
]

membership = [
    url(r'^(?P<pk>\d+)/$', views.MembershipDetail.as_view(), name='membership-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.MembershipEdit.as_view(), name='membership-edit'),
]

group = [
    url(r'^$', views.GroupList.as_view(), name='group-list'),
    url(r'^(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='group-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.GroupEdit.as_view(), name='group-edit'),
]

urlpatterns = [
    url(r'^person/', include(person)),
    url(r'^recipient/', include(recipient)),
    url(r'^volunteer/', include(volunteer)),
    url(r'^member/', include(member)),
    url(r'^custodian/', include(custodian)),
    url(r'^membership/', include(membership)),
    url(r'^group/', include(group)),

    url(r'^$', RedirectView.as_view(url='login/')),
    url(r'^missing_doc/$', views.missing_doc, name='missing_doc'),

    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.LogOut.as_view(), name='logout'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^basicformnewperson/$', views.NewIndividualMember.as_view(), name='basicformnewperson'),
    url(r'^basicformnewfamily/$', views.NewFamilyMember.as_view(), name='basicformnewfamily'),
    url(r'^membership/$', views.MembershipList.as_view(), name='membership-list'),
    url(r'^membership/(?P<pk>[^/]+)/$', views.MembershipDetail.as_view(), name='membership-detail'),

]
