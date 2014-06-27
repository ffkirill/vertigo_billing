# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm, DecimalField, CharField, BooleanField, \
    ModelChoiceField
from django.forms import Textarea, HiddenInput
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from common.forms import VertigoBootstrapMixin
from .models import Movement, Account


class AccountRechargeModelForm(VertigoBootstrapMixin, ModelForm):
    class Meta:
        model = Movement
        exclude = ('credit, balance',)

    account = ModelChoiceField(
        queryset=Account.objects.select_related('person').order_by(
            'person__string_value'),
        label=_('Account'))

    debit = DecimalField(label=_("Amount"),
                         max_digits=10,
                         decimal_places=2,
                         required=True)

    description = CharField(label=_("Operation description"),
                            widget=Textarea,
                            initial=_("Account recharge"))

    confirm = BooleanField(initial=False,
                           widget=HiddenInput,
                           required=False)

    def clean(self):
        d = super(AccountRechargeModelForm, self).clean()
        if not self.errors and not d['confirm']:
            data = self.data.copy()
            data['confirm'] = True
            self.data = data
            raise ValidationError(_("Data is correct. "
                                    "Please check again payment details"
                                    " and resubmit form"))
        return d




