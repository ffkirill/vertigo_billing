# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

_("Clients")


class Person(models.Model):
    """Person.
    """

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['string_value']

    name = models.CharField(verbose_name=_("Name"),
                            max_length=100,
                            db_index=True)

    surname = models.CharField(verbose_name=_("Surname"),
                               max_length=100,
                               blank=True,
                               db_index=True)

    last_name = models.CharField(verbose_name=_("Last name"),
                                 max_length=100,
                                 blank=True)

    phone = models.CharField(verbose_name=_("Phone number"),
                             max_length=50,
                             blank=True)

    email = models.EmailField(verbose_name=_("Email"),
                              blank=True,
                              error_messages={
                                  'invalid': _('Enter a valid email address.')
                              }
    )

    comment = models.CharField(verbose_name=_("Comment"),
                               max_length=300,
                               blank=True)

    string_value = models.CharField(editable=False,
                                    max_length=100)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if update_fields is not None:
            if frozenset(('name', 'surname', 'last_name')) \
               & frozenset(update_fields):
                update_fields.append('string_value')
                self.string_value = unicode(self)
        else:
            self.string_value = unicode(self)

        super(Person, self).save(force_insert, force_update, using,
                                 update_fields)

    def get_absolute_url(self):
        return reverse_lazy('clients:detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        if self.surname:
            return "{0} {1}.{2}".format(
                self.surname.strip(),
                self.name.strip()[0],
                " {0}.".format(self.last_name.strip()[0])
                if self.last_name else "")
        else:
            return self.name.strip()