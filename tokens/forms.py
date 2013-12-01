from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import VertigoBootstrapMixin, VertigoModelForm

from .models import Token, TokenReader


class ModelByFieldValueField(forms.CharField):
    error_message = None
    key = None
    queryset = None

    def to_python(self, value):
        value = super(ModelByFieldValueField, self).to_python(value)
        try:
            value = self.queryset.get(**{self.key: value})
        except(ValueError, self.queryset.model.DoesNotExist):
            raise forms.ValidationError(self.error_message)
        return value


class TokenByValueFormField(ModelByFieldValueField):
    error_message = _("Invalid token value")
    key = "value"
    queryset = Token.objects.active()

    def validate(self, value):
        super(TokenByValueFormField, self).validate(value)
        if value.person.account.disabled:
            raise forms.ValidationError(_("Person account is locked"))


class TokenReaderByUIDFormField(ModelByFieldValueField):
    error_message = _("Invalid token reader uid")
    key = "uid"
    queryset = TokenReader.objects.active()


class ProcessRFIDTokenForm(VertigoBootstrapMixin, forms.Form):
    reader = TokenReaderByUIDFormField()
    token = TokenByValueFormField()


class TokenModelForm(VertigoModelForm):
    class Meta:
        model = Token


class TokenReaderModelForm(VertigoModelForm):
    class Meta:
        model = TokenReader