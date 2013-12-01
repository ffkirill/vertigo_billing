from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns(
    '',
    url(r'^logout/$', logout, name="logout"),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('messaging:messages')),
        name="main"),
)
