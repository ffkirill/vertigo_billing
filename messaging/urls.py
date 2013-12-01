from django.conf.urls import patterns, url
from .views import MessageListView, MarkMessagesReadView

urlpatterns = patterns(
    '',
    url(r'^$', MessageListView.as_view(), name="messages"),
    url(r'^mark_read/$', MarkMessagesReadView.as_view(), name="mark_read"),
)
