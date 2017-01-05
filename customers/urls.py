
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    ProfileBasic, ProfilePhoneNumber, ProfileVerifyPhoneNumber,
    ProfileCompanyCreateView, ProfileCompanyVerifyView
)

profile_root = TemplateView.as_view(template_name='profile.html')

urlpatterns = [
    url(r'accounts/profile/$',
        profile_root,
        name='account_profile'),

    url(r'accounts/profile/basic/$',
        ProfileBasic.as_view(),
        name='account_basic_info'),

    url(r'accounts/profile/phone/$',
        ProfilePhoneNumber.as_view(),
        name='account_phone_number'),

    url(r'accounts/profile/phone/verify/$',
        ProfileVerifyPhoneNumber.as_view(),
        name='account_phone_number_verify'),

    url(r'accounts/profile/company/$',
        ProfileCompanyCreateView.as_view(),
        name='account_company_details'),

    url(r'accounts/profile/company/verify/$',
        ProfileCompanyVerifyView.as_view(),
        name='account_company_details_verify'),
]
