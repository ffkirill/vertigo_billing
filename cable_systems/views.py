from __future__ import unicode_literals
from django.views.generic import ListView, CreateView, DeleteView, \
    UpdateView

from braces.views import PermissionRequiredMixin, OrderableListMixin

from .forms import CableModelForm
from .models import CableSystem, CableSystemSession

from common.views import ListViewQMixin, SuccessURLInRequestMixin, DisableView


class CableListView(ListViewQMixin,
                    OrderableListMixin,
                    ListView):
    model = CableSystem
    filter_query_field = 'name__icontains'
    orderable_columns = ('pk',
                         'name',
                         'rate')
    orderable_columns_default = 'pk'
    paginate_by = 5


class SessionListView(ListViewQMixin,
                      OrderableListMixin,
                      ListView):
    model = CableSystemSession
    orderable_columns = ('date_start', 'date_end', 'cable', 'person',
                         'active')
    orderable_columns_default = '-date_end'
    filter_expr = staticmethod(CableSystemSession.filter_expr)
    paginate_by = 15


class CableCreateView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      CreateView):
    model = CableSystem
    form_class = CableModelForm
    permission_required = 'cable_systems.add_cablesystem'


class CableChangeView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      UpdateView):
    model = CableSystem
    form_class = CableModelForm
    permission_required = 'cable_systems.change_cablesystem'


class CableDeleteView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = CableSystem
    permission_required = 'cable_systems.delete_cablesystem'


class CableDisableView(PermissionRequiredMixin, DisableView):
    model = CableSystem
    permission_required = 'cable_systems.change_cablesystem'
