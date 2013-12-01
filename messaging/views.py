from django.views.generic import ListView, FormView
from common.views import RangeBasedViewMixin
from django.forms import Form
from django.forms.models import ModelChoiceField
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin
from .models import Message, UsersMessages


class BaseMessageListView(ListView):
    model = Message

    def get_queryset(self):
        return self.request.user.received_messages.all()\
            .extra(select={'unread': 'messaging_usersmessages.unread'})\
            .order_by('-unread', '-date')


class MessageListView(LoginRequiredMixin,
                      RangeBasedViewMixin,
                      BaseMessageListView):

    paginate_by = 10


class MarkMessagesReadForm(Form):
    message = ModelChoiceField(
        queryset=Message.objects.filter(usersmessages__unread=True),
        required=False)


class MarkMessagesReadView(LoginRequiredMixin,
                           FormView):

    form_class = MarkMessagesReadForm
    success_url = reverse_lazy('messaging:messages')

    def form_valid(self, form):
        qs = UsersMessages.objects.filter(user=self.request.user, unread=True)
        if form.cleaned_data['message']:
            qs = qs.filter(message=form.cleaned_data['message'])
        qs.update(unread=False)
        return super(MarkMessagesReadView, self).form_valid(form)