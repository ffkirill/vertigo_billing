from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.views.generic import FormView, ListView, CreateView, DeleteView, \
    UpdateView, TemplateView

from braces.views import PermissionRequiredMixin, LoginRequiredMixin, \
    MultiplePermissionsRequiredMixin, SelectRelatedMixin

import json
from django.http import HttpResponse

from .forms import ProcessRFIDTokenForm, TokenModelForm, TokenReaderModelForm
from .models import Token, TokenReader
from cable_systems.models import CableSystemSession
from common.views import ListViewQMixin, SuccessURLInRequestMixin, DisableView
from messaging.models import Message

User = get_user_model()


class TokenListView(ListViewQMixin,
                    SelectRelatedMixin,
                    ListView):
    model = Token
    filter_expr = staticmethod(Token.filter_expr)
    paginate_by = 5
    select_related = ('person',)


class ReaderListView(ListViewQMixin,
                     SelectRelatedMixin,
                     ListView):
    model = TokenReader
    filter_expr = staticmethod(TokenReader.filter_expr)
    paginate_by = 5
    select_related = ('cable_system',)


class TokenCreateView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      CreateView):
    model = Token
    form_class = TokenModelForm
    permission_required = 'tokens.add_token'


class ReaderCreateView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       CreateView):
    model = TokenReader
    form_class = TokenReaderModelForm
    permission_required = 'tokens.add_tokenreader'


class TokenChangeView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      UpdateView):
    model = Token
    form_class = TokenModelForm
    permission_required = 'tokens.change_token'


class ReaderChangeView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       UpdateView):
    model = TokenReader
    form_class = TokenReaderModelForm
    permission_required = 'tokens.change_tokenreader'


class TokenDeleteView(SuccessURLInRequestMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = Token
    permission_required = 'tokens.delete_token'


class ReaderDeleteView(SuccessURLInRequestMixin,
                       PermissionRequiredMixin,
                       DeleteView):
    model = TokenReader
    permission_required = 'tokens.delete_tokenreader'


class TokenDisableView(PermissionRequiredMixin, DisableView):
    model = Token
    permission_required = 'tokens.change_token'


class ReaderDisableView(PermissionRequiredMixin, DisableView):
    model = TokenReader
    permission_required = 'tokens.change_tokenreader'


class ProcessTokenView(MultiplePermissionsRequiredMixin, FormView):
    template_name = 'tokens/process.html'
    template_success = 'tokens/process_success.html'
    form_class = ProcessRFIDTokenForm
    permissions = {
        'all': ('cable_systems.add_cablesystemsession',
                'cable_systems.change_cablesystemsession',)
    }

    @staticmethod
    def render_to_json_response(context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def render_on_success(self, **context):
        self.template_name = self.template_success
        return self.render_to_response(context)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return super(ProcessTokenView, self).form_invalid(form)

    def form_valid(self, form):
        person = form.cleaned_data['token'].person
        cable = form.cleaned_data['reader'].cable_system
        session, cost = CableSystemSession.objects.toggle_active(person=person,
                                                                 cable=cable)
        if session.person.account.balance < 0:
            Message.create_message(
                body=_("Insufficient funds to pay for use of the system"),
                recipients=list(User.objects.filter(is_staff=True,
                                                    is_active=True)),
                content_object=session.person,
                request=self.request)

        if self.request.is_ajax():
            data = {'person': unicode(session.person),
                    'cable': unicode(cable),
                    'active': session.active}
            return self.render_to_json_response(data)

        return self.render_on_success(person=session.person,
                                      cable=cable,
                                      active=session.active)


class TokenReaderView(LoginRequiredMixin, TemplateView):
    template_name = "tokens/token_reader.html"
    form_class = ProcessRFIDTokenForm
