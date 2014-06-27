from django.conf.urls import patterns, url
from .views import CableListView, CableCreateView, CableChangeView, \
    CableDeleteView, CableDisableView, SessionListView

urlpatterns = patterns(
    '',
    url(r'^$', CableListView.as_view(), name="cables"),
    url(r'^add/$', CableCreateView.as_view(), name="add_cable"),
    url(r'^change/(?P<pk>\d+)/$', CableChangeView.as_view(),
        name="change_cable"),
    url(r'^delete/(?P<pk>\d+)/$', CableDeleteView.as_view(),
        name="delete_cable"),
    url(r'^disable/(?P<pk>\d+)/$', CableDisableView.as_view(),
        name="disable_cable"),

    url(r'^sessions/$', SessionListView.as_view(), name="sessions"),
)
