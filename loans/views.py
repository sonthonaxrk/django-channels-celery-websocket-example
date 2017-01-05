from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from loans.models import Loan
from loans.forms import LoanForm


class LoanViewMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.profile_complete:
            messages.add_message(
                self.request, messages.INFO,
                'You must complete registration before creating a loan.'
            )
            return redirect('account_profile')

        return super().dispatch(*args, **kwargs)


class LoanIndexView(LoanViewMixin, ListView):
    model = Loan
    template_name = 'loan_index.html'
    context_object_name = 'loans'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.company.loan_set.all()


class LoanDetailView(LoanViewMixin, DetailView):
    model = Loan
    template_name = 'loan_detail.html'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.company.loan_set.all()

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['loan_id'])
        except Loan.DoesNotExist:
            raise Http404


class LoanCreateView(LoanViewMixin, CreateView):
    model = Loan
    template_name = 'loan_create.html'
    form_class = LoanForm
    success_url = reverse_lazy('loan_index')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.save()
        return super().form_valid(form)
