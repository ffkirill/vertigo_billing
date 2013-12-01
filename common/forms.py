from bootstrap.forms import BootstrapModelForm, BootstrapMixin


class VertigoModelForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(VertigoModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class VertigoBootstrapMixin(BootstrapMixin):
    def __init__(self, *args, **kwargs):
        super(VertigoBootstrapMixin, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
