from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.group_list), 
    url(r'^groups/(?P<pk>\d+)/$', views.group_detail), 
    url(r'^person/', views.person_list),
    url(r'^person/(?P<pk>\d+)/$',views.person_detail),
    
]
