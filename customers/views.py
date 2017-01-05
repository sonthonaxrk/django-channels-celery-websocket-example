from random import randint

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect

from twilio import TwilioRestException

from customers.models import Customer, Company
from customers.forms import (
    CompanyDetailsConfirmForm, UserDetailsConfirmForm, PhoneNumberConfirmForm,
    PhoneNumberVerifyForm, CompanyDetailsVerifyForm
)

from customers.tasks import send_phone_code

from django.views.generic.edit import UpdateView, CreateView, FormView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy


class ProfileViewMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.request = self.request
        return form

    def get_object(self, queryset=None):
        return self.request.user


class ProfileBasic(ProfileViewMixin, UpdateView):
    form_class = UserDetailsConfirmForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('account_profile')
    model = Customer

    def form_valid(self, form):
        form.instance.confirmed_name = True
        messages.add_message(
            self.request, messages.INFO,
            'Successfully Updated User Name'
        )
        return super().form_valid(form)


class ProfilePhoneNumber(ProfileViewMixin, UpdateView):
    form_class = PhoneNumberConfirmForm
    template_name = 'profile_form.html'
    model = Customer

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        verify_token = '{0:04d}'.format(
            randint(0, 9999)
        )

        task = send_phone_code.delay(
            self.request.user.id, verify_token, phone_number
        )

        self.request.session['active_phone_number_task_id'] = task.id
        self.request.session['processing_phone_number'] = phone_number
        self.request.session['verify_token'] = verify_token

        return redirect('account_phone_number_verify')


class ProfileVerifyPhoneNumber(ProfileViewMixin, FormView):
    form_class = PhoneNumberVerifyForm
    template_name = 'profile_verify_phone.html'
    success_url = reverse_lazy('account_profile')

    def form_valid(self, form):
        user = self.request.user
        user.phone_number = self.request.session['processing_phone_number']
        user.confirmed_phone_number = True

        messages.add_message(
            self.request, messages.INFO,
            'Successfully Verified Phone Number'
        )

        user.save()

        return super().form_valid(form)


class ProfileCompanyCreateView(ProfileViewMixin, CreateView):
    template_name = 'profile_form.html'
    model = Company
    form_class = CompanyDetailsConfirmForm
    success_url = reverse_lazy('account_company_details_verify')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        company = getattr(self.request.user, 'company')
        if company and getattr(company, 'verified'):
            messages.add_message(
                self.request, messages.INFO,
                'You already have a company'
            )
            return redirect('account_profile')

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        company = form.instance
        self.request.user.company = company
        self.request.user.save()
        return super().form_valid(form)


class ProfileCompanyVerifyView(ProfileViewMixin, UpdateView):
    template_name = 'profile_company_verify.html'
    model = Company
    form_class = CompanyDetailsVerifyForm
    success_url = reverse_lazy('account_profile')

    def get_object(self, queryset=None):
        return self.request.user.company

    def form_valid(self, form):
        form.instance.verified = True
        form.save()
        return super().form_valid(form)
