from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from common.forms import VertigoModelForm
from .models import Person
from tokens.models import Token
from django.forms.models import ModelChoiceField
from django.forms.util import ErrorList


class PersonModelForm(VertigoModelForm):
    class Meta:
        model = Person

    token = ModelChoiceField(
        label=_("RFID Token"),
        queryset=Token.objects,
        required=False
    )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        super(PersonModelForm, self).__init__(data, files, auto_id, prefix,
                                              initial, error_class,
                                              label_suffix,
                                              empty_permitted, instance)
        if instance and hasattr(instance, 'token'):
            self.initial['token'] = instance.token.pk

    def save(self, commit=True):
        r = super(PersonModelForm, self).save(commit)
        token = self.cleaned_data['token']
        if token:
            token.person = self.instance
            token.save()
        else:
            Token.objects.filter(person=self.instance).update(person=None)
        return r
