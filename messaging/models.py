from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from common.models import QuerySet
from .utils import send_notification


class MessagesQuerySet(QuerySet):

    def unread(self):
        return self.filter(usersmessages__unread=True)

    def read(self):
        return self.filter(usersmessages__unread=False)


class Message(models.Model):

    objects = MessagesQuerySet.as_manager()

    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(_("Message body"), blank=True)
    sender = models.ForeignKey(get_user_model(),
                               related_name='sent_messages',
                               null=True,
                               blank=True,
                               verbose_name=_("sender"))

    content_type = models.ForeignKey(ContentType,
                                     null=True,
                                     blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    recipients = models.ManyToManyField(
        get_user_model(),
        through='UsersMessages',
        related_name='received_messages',
        null=True,
        blank=True,
        verbose_name=_("recipients"))

    @classmethod
    @transaction.atomic
    def create_message(cls, body, recipients, sender=None, content_object=None,
                       request=None):
        m = cls.objects.create(sender=sender, body=body,
                               content_object=content_object)
        for recipient in recipients:
            UsersMessages.objects.create(user=recipient, message=m)
        if request:
            try:
                send_notification(unicode(request.session.session_key),
                                  m,
                                  recipients)
            except IOError:
                pass

    def __unicode__(self):
        return self.body


class UsersMessages(models.Model):
    user = models.ForeignKey(get_user_model())
    message = models.ForeignKey(Message)
    unread = models.BooleanField(default=True,
                                 null=False)

    def mark_read(self):
        type(self).objects.filter(pk=self.pk).update(unread=False)
        self.unread = False

    def mark_unread(self):
        type(self).objects.filter(pk=self.pk).update(unread=True)
        self.unread = True

    class Meta:
        unique_together = [("user", "message")]

