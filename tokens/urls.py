from django.conf.urls import patterns, url
from .views import ProcessTokenView, TokenListView, TokenCreateView, \
    TokenChangeView, TokenDeleteView, TokenDisableView
from .views import ReaderListView, ReaderCreateView, ReaderChangeView, \
    ReaderDeleteView, ReaderDisableView
from .views import TokenReaderView

urlpatterns = patterns(
    '',
    url(r'^$', TokenListView.as_view(), name="tokens"),
    url(r'^add/$', TokenCreateView.as_view(), name="add_token"),
    url(r'^change/(?P<pk>\d+)/$', TokenChangeView.as_view(),
        name="change_token"),
    url(r'^delete/(?P<pk>\d+)/$', TokenDeleteView.as_view(),
        name="delete_token"),
    url(r'^disable/(?P<pk>\d+)/$', TokenDisableView.as_view(),
        name="disable_token"),

    url(r'^readers/$', ReaderListView.as_view(), name="readers"),
    url(r'^readers/add/$', ReaderCreateView.as_view(), name="add_reader"),
    url(r'^readers/change/(?P<pk>\d+)/$', ReaderChangeView.as_view(),
        name="change_reader"),
    url(r'^readers/delete/(?P<pk>\d+)/$', ReaderDeleteView.as_view(),
        name="delete_reader"),
    url(r'^readers/disable/(?P<pk>\d+)/$', ReaderDisableView.as_view(),
        name="disable_reader"),

    url(r'^process/$', ProcessTokenView.as_view(), name="process"),
    url(r'^token_reader/$', TokenReaderView.as_view(), name="token_reader"),
)
