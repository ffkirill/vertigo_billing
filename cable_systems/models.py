# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from common.models import ModelWithDisabledMark
from accounting.models import Movement
from django.utils import timezone
from decimal import Decimal

_("Cable_Systems")


class CableSystem(ModelWithDisabledMark):
    """Wakeboard cable system
    """
    class Meta:
        verbose_name = _("Cable system")
        verbose_name_plural = _("Cable systems")
        ordering = ['name']

    name = models.CharField(verbose_name=_("Cable system's name"),
                            max_length=100)

    rate = models.DecimalField(verbose_name=_("Per hour pay rate"),
                               max_digits=8,
                               decimal_places=2)

    def __unicode__(self):
        return self.name


class CableSystemSessionManager(models.Manager):

    @transaction.atomic
    def toggle_active(self, person, cable):
        qs = self.select_for_update().filter(cable=cable,
                                             active=True)
        cost = 0
        if qs.exists():
            sess = qs[0]
            sess.date_end = timezone.now()
            sess.active = False
            sess.save()
            sess_timedelta = sess.date_end - sess.date_start
            cost = sess_timedelta.days * Decimal(24) * cable.rate \
                + Decimal(sess_timedelta.seconds) / Decimal(60.0) \
                / Decimal(60.0) * cable.rate

            Movement.objects.create(
                account=sess.person.account,
                credit=cost,
                description=_("Cable system use")
            )

        else:
            sess = self.create(cable=cable,
                               person=person,
                               date_start=timezone.now(),
                               date_end=timezone.now(),
                               active=True)

        return sess, cost


class CableSystemSession(models.Model):
    """Cable system session
    """
    objects = CableSystemSessionManager()

    class Meta:
        verbose_name = _("Cable system session")
        verbose_name_plural = _("Cable systems session")
        ordering = ['date_end', 'date_start']

    cable = models.ForeignKey(CableSystem, verbose_name=_("Cable system"))
    person = models.ForeignKey('clients.Person', verbose_name=_("Person"))
    date_start = models.DateTimeField(verbose_name=_("Start date and time"))
    date_end = models.DateTimeField(verbose_name=_("End date and time"))
    active = models.BooleanField(verbose_name=_("Active"),
                                 null=False,
                                 blank=False)

    @staticmethod
    def filter_expr(q):
        return (Q(cable__name__icontains=q)
                | Q(person__string_value__icontains=q))
