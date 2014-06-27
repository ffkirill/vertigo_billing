from django.views.generic import DeleteView
from django.http.response import HttpResponseRedirect
from django.forms import Form, DateField
from collections import defaultdict

_ORDERING_DICT = defaultdict(str, {'desc': '-'})


class ListViewQMixin(object):
    filter_query_field = None
    filter_expr = None

    def get_queryset(self):
        qs = super(ListViewQMixin, self).get_queryset()
        q = self.request.REQUEST.get('Q')
        if q:
            qs = (qs.filter(**{self.filter_query_field: q})
                  if not self.filter_expr else qs.filter(self.filter_expr(q)))
        return qs

    def get_context_data(self, **kwargs):
        cd = super(ListViewQMixin, self).get_context_data(**kwargs)
        cd['Q'] = self.request.REQUEST.get('Q', "")
        cd['show_Q'] = True
        return cd


class RangeBasedViewMixin(object):
    date_field = "date"

    class RangeForm(Form):
        date_start = DateField(required=False)
        date_end = DateField(required=False)

    def __init__(self):
        self.date_start = None
        self.date_end = None
        super(RangeBasedViewMixin, self).__init__()

    def get_queryset(self):
        qs = super(RangeBasedViewMixin, self).get_queryset()
        range_form = self.RangeForm(self.request.REQUEST)
        if range_form.is_valid():
            self.date_start = range_form.cleaned_data['date_start']
            self.date_end = range_form.cleaned_data['date_end']
        if self.date_start:
            qs = qs.filter(**{self.date_field + "__gte": self.date_start})
        if self.date_end:
            qs = qs.filter(**{self.date_field + "__lte": self.date_end})
        return qs

    def get_context_data(self, **kwargs):
        cd = super(RangeBasedViewMixin, self).get_context_data(**kwargs)
        range_form = self.RangeForm({
            'date_start': self.date_start,
            'date_end': self.date_end
        })
        cd['date_start'] = range_form['date_start'].value()
        cd['date_end'] = range_form['date_end'].value()
        cd['show_datepicker'] = True
        return cd


class ListViewSortMixin(ListViewQMixin):
    order_by_param = 'order_by',
    direction_param = 'order'
    possible_order_fields = None

    def get_queryset(self):
        qs = super(ListViewQMixin, self).get_queryset()
        direction = _ORDERING_DICT[
            self.request.REQUEST.get(self.direction_param)
        ]

        field = self.request.REQUEST.get(self.order_by_param)

        if (field and
                self.possible_order_fields and
                field in self.possible_order_fields or
                field and self.possible_order_fields is None):
            qs = qs.order_by([direction + field])
        return qs

    def get_context_data(self, **kwargs):
        cd = super(ListViewQMixin, self).get_context_data(**kwargs)
        cd['Q'] = self.request.REQUEST.get('Q', "")
        return cd


class SuccessURLInRequestMixin(object):
    def __get_success_url(self):
        return getattr(self, 'success_url', '')

    def get_context_data(self, **kwargs):
        cd = super(SuccessURLInRequestMixin, self).get_context_data(**kwargs)
        cd['next'] = self.request.GET.get('next', self.__get_success_url())
        return cd

    def get_success_url(self):
        self.success_url = self.request.GET.get('next',
                                                self.__get_success_url())
        return super(SuccessURLInRequestMixin, self).get_success_url()


class DisableView(SuccessURLInRequestMixin, DeleteView):
    template_name_suffix = '_confirm_disable'

    def delete(self, request, *args, **kwargs):
        ob = self.get_object()
        self.object = ob
        if ob.disabled:
            ob.enable()
        else:
            ob.disable()
        return HttpResponseRedirect(self.get_success_url())


