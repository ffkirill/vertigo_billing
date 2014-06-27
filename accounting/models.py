# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal
from clients.models import Person

from common.models import ModelWithDisabledMark

_("Accounting")


class Account(ModelWithDisabledMark):
    """Person's account
    """

    class Meta:
        verbose_name = _("Person's account")
        verbose_name_plural = _("Accounts")
        ordering = ['person']

    person = models.OneToOneField("clients.Person",
                                  verbose_name=_("Person"))

    balance = models.DecimalField(verbose_name=_("Balance"),
                                  max_digits=10,
                                  decimal_places=2,
                                  blank=True,
                                  null=True,
                                  default=0)

    def __unicode__(self):
        return "{0}: {1}".format(self.person, self.balance)


@receiver(post_save, sender=Person)
def on_person_create(instance, raw, created, using, **kwargs):
    if created and not raw:
        Account.objects.using(using).create(person=instance)


class Movement(models.Model):
    """Account's movement
    """

    class Meta:
        verbose_name = _("Account's movement")
        verbose_name_plural = _("Accounts movements")
        ordering = ['date']

    account = models.ForeignKey(Account,
                                verbose_name=_("Account"))

    date = models.DateTimeField(auto_now_add=True)

    debit = models.DecimalField(verbose_name=_("Debit"),
                                max_digits=10,
                                decimal_places=2,
                                blank=True,
                                null=True,
                                default=0)

    credit = models.DecimalField(verbose_name=_("Credit"),
                                 max_digits=10,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 default=0)

    balance = models.DecimalField(verbose_name=_("Balance"),
                                  max_digits=10,
                                  decimal_places=2,
                                  blank=True,
                                  null=True,
                                  default=0)

    def balance_before(self):
        return self.balance - self.debit + self.credit

    description = models.CharField(verbose_name=_("Operation description"),
                                   max_length=300,
                                   blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        with transaction.atomic(using=using):
            force_insert = force_insert or self.pk is None
            if force_insert:
                account_data = Account.objects.using(using) \
                    .select_for_update().filter(pk=self.account.pk) \
                    .values('balance', 'disabled')[0]

                if account_data['disabled']:
                    raise IntegrityError(
                        "Attempted to make a movement on disabled account")

                self.balance = Decimal(account_data['balance']
                                       + self.debit
                                       - self.credit).quantize(Decimal('0.00'))

                Account.objects.using(using).filter(pk=self.account.pk).update(
                    balance=self.balance)

            super(Movement, self).save(force_insert, force_update, using,
                                       update_fields)

    def __unicode__(self):
        return "{0} Dt:{1} Ct:{2} Bal:{3} Desc:{4}".format(
            self.account.person,
            self.debit,
            self.credit,
            self.balance,
            self.description
        )
