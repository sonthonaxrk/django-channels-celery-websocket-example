from django.conf.urls import url

from loans.views import LoanIndexView, LoanDetailView, LoanCreateView

urlpatterns = [
    url(r'loans/$',
        LoanIndexView.as_view(),
        name='loan_index'),

    url(r'loans/(?P<loan_id>[0-9]+)/$',
        LoanDetailView.as_view(),
        name='loan_detail'),

    url(r'loans/create/$',
        LoanCreateView.as_view(),
        name='loan_create'),
]
