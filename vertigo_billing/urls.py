from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
   (r'^bootstrap\.html/$',
    TemplateView.as_view(template_name="bootstrap.html")),
   (
       r'^tokens/', include('tokens.urls', namespace='tokens')),
   (r'^cables/', include('cable_systems.urls',
                         namespace='cable_systems')),
   (r'^clients/',
    include('clients.urls', namespace='clients')),
   (r'^accounting/',
    include('accounting.urls', namespace='accounting')),
   (r'^messages/',
    include('messaging.urls', namespace='messaging')),
   (r'^', include('common.urls', namespace='common')),


   # Uncomment the next line to enable the admin:
   url(r'^admin/', include(admin.site.urls)),
)