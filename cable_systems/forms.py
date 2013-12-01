from common.forms import VertigoModelForm
from .models import CableSystem


class CableModelForm(VertigoModelForm):
    class Meta:
        model = CableSystem