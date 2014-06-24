# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


class ModelWithDisabledMarkManager(models.Manager):
    def active(self):
        return self.filter(disabled=False)


class ModelWithDisabledMark(models.Model):

    objects = ModelWithDisabledMarkManager()

    class Meta:
        abstract = True

    disabled = models.BooleanField(verbose_name=_("Disabled"),
                                   null=False,
                                   blank=False,
                                   default=False)

    def disable(self):
        self.disabled = True
        self.__class__.objects.filter(pk=self.pk).update(disabled=True)

    def enable(self):
        self.disabled = False
        self.__class__.objects.filter(pk=self.pk).update(disabled=False)


class QuerySetManager(models.Manager):
    # http://docs.djangoproject.com/en/dev/topics/db/managers/#using-managers-for-related-object-access
    # Not working cause of:
    # http://code.djangoproject.com/ticket/9643
    use_for_related_fields = True

    def __init__(self, qs_class=models.query.QuerySet):
        self.queryset_class = qs_class
        super(QuerySetManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class QuerySet(models.query.QuerySet):
    """Base QuerySet class for adding custom methods that are made
    available on both the manager and subsequent cloned QuerySets"""

    @classmethod
    def as_manager(cls, manager_class=QuerySetManager):
        return manager_class(cls)
