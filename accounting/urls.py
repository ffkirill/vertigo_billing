from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import AccountDisableView
from .views import AccountRechargeView
from .views import MovementListView

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url=reverse_lazy("accounting:movements")),
        name="accounting"),
    url(r'^recharge/$', AccountRechargeView.as_view(), name="recharge"),
    url(r'^movements/$', MovementListView.as_view(), name="movements"),
    url(r'^disable/(?P<pk>\d+)/$', AccountDisableView.as_view(),
        name="disable"),
)
