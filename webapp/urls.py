from django.conf.urls import include, url
from django.views.generic import RedirectView

from . import views

person = [
    url(r'^$', views.PersonList.as_view(), name='person-list'),
    url(r'^(?P<pk>[^/]+)/$', views.PersonDetail.as_view(), name='person-detail'),
    url(r'^(?P<pk>[^/]+)/edit/$', views.PersonEdit.as_view(), name='person-edit'),
]

recipient = [
    url(r'^(?P<pk>\d+)/$', views.RecipientDetail.as_view(), name='recipient-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.RecipientEdit.as_view(), name='recipient-edit'),
]

volunteer = [
    url(r'^(?P<pk>\d+)/$', views.VolunteerDetail.as_view(), name='volunteer-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.VolunteerEdit.as_view(), name='volunteer-edit'),
]

urlpatterns = [
    url(r'^person/', include(person)),
    url(r'^recipient/', include(recipient)),
    url(r'^volunteer/', include(volunteer)),

    url(r'^$', RedirectView.as_view(url='login/')),
    url(r'^groups/(?P<pk>\d+)/$', views.group_detail, name='group_detail'),
    url(r'^missing_doc/$', views.missing_doc, name='missing_doc'),

    url(r'^login/$', views.login),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^basicformnewperson/$', views.NewIndividualMember.as_view(), name='basicformnewperson'),
    url(r'^basicformnewfamily/$', views.NewFamilyMember.as_view(), name='basicformnewfamily'),
    url(r'^membership/$', views.MembershipList.as_view(), name='membership-list'),
    url(r'^membership/(?P<pk>[^/]+)/$', views.MembershipDetail.as_view(), name='membership-detail'),

]
