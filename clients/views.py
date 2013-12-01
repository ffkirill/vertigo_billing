from django.views.generic import ListView, DeleteView, CreateView, UpdateView, \
    DetailView
from .models import Person
from .forms import PersonModelForm
from braces.views import PermissionRequiredMixin, OrderableListMixin, \
    SelectRelatedMixin
from common.views import SuccessURLInRequestMixin
from common.views import ListViewQMixin


class PersonsListView(SelectRelatedMixin,
                      ListViewQMixin,
                      OrderableListMixin,
                      ListView):
    model = Person
    paginate_by = 5
    filter_query_field = 'string_value__icontains'
    orderable_columns = ('string_value',
                         'name',
                         'surname',
                         'last_name',
                         'account__pk',
                         'account__balance')
    orderable_columns_default = 'string_value'
    select_related = ('account',
                      'token',)


class PersonCreateView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       CreateView):
    model = Person
    Person.objects.order_by()
    form_class = PersonModelForm
    permission_required = 'clients.add_person'


class PersonChangeView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       UpdateView):
    model = Person
    form_class = PersonModelForm
    permission_required = 'clients.change_person'


class PersonDeleteView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       DeleteView):
    model = Person
    permission_required = 'clients.delete_person'


class PersonDetailView(SuccessURLInRequestMixin,
                       DetailView):
    model = Person



