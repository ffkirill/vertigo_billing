from django.views.generic import CreateView, ListView, DateDetailView
from django.core.urlresolvers import reverse_lazy
from common.views import DisableView
from common.views import SuccessURLInRequestMixin
from common.views import RangeBasedViewMixin
from braces.views import PermissionRequiredMixin, OrderableListMixin, \
    SelectRelatedMixin
from .models import Account, Movement
from .forms import AccountRechargeModelForm


class AccountDisableView(PermissionRequiredMixin, DisableView):
    model = Account
    permission_required = 'accounting.account_change'


class AccountRechargeView(PermissionRequiredMixin,
                          SuccessURLInRequestMixin,
                          CreateView):
    model = Movement
    form_class = AccountRechargeModelForm
    template_name = 'accounting/recharge.html'
    permission_required = 'accounting.movement_add'
    success_url = reverse_lazy('accounting:accounting')

    def get_initial(self):
        initial = super(AccountRechargeView, self).get_initial()
        acc = self.request.REQUEST.get('account', None)
        if acc:
            initial['account'] = acc
        return initial


class MovementListView(OrderableListMixin,
                       RangeBasedViewMixin,
                       SelectRelatedMixin,
                       ListView):
    model = Movement
    paginate_by = 10
    orderable_columns = ['account', 'date', 'account__person']
    orderable_columns_default = '-date'
    select_related = ('account','account__person',)