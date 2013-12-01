# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from common.models import ModelWithDisabledMark

_("Tokens")


class Token(ModelWithDisabledMark):
    """RFID Token.
    """
    class Meta:
        verbose_name = _("RFID Token")
        verbose_name_plural = _("RFID Tokens")
        ordering = ["name"]

    name = models.CharField(verbose_name=_("Token name"), max_length=100)
    value = models.CharField(verbose_name=_("Token value"), max_length=100)
    person = models.OneToOneField("clients.Person",
                                  verbose_name=_("Token owner"),
                                  blank=True,
                                  null=True)

    @staticmethod
    def filter_expr(q):
        return (Q(person__string_value__icontains=q) | Q(name__icontains=q)
                | Q(value__icontains=q))

    def __unicode__(self):
        return (_("Token: {0}").format(self.name) +
                (". " + _("Owner: {0}").format(unicode(self.person))
                 if self.person else ""))


class TokenReader(ModelWithDisabledMark):
    """RFID Token reader.
    """
    class Meta:
        verbose_name = _("RFID Token reader")
        verbose_name_plural = _("RFID Token readers")
        ordering = ["description"]

    uid = models.CharField(verbose_name=_("Reader id"),
                           unique=True,
                           max_length=100)

    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100)

    cable_system = models.ForeignKey('cable_systems.CableSystem',
                                     verbose_name=_("Cable system"))

    @staticmethod
    def filter_expr(q):
        return (Q(uid__icontains=q) | Q(description__icontains=q)
                | Q(cable_system__name__icontains=q))

    def __unicode__(self):
        return self.description