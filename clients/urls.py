from django.conf.urls import patterns, url
from .views import PersonsListView, PersonCreateView, PersonChangeView,\
    PersonDeleteView, PersonDetailView

urlpatterns = patterns(
    '',
    url(r'^$', PersonsListView.as_view(), name="clients"),
    url(r'^add/$', PersonCreateView.as_view(), name="add"),
    url(r'^(?P<pk>\d+)/$', PersonDetailView.as_view(), name="detail"),
    url(r'^change/(?P<pk>\d+)/$', PersonChangeView.as_view(), name="change"),
    url(r'^delete/(?P<pk>\d+)/$', PersonDeleteView.as_view(), name="delete"),
)
