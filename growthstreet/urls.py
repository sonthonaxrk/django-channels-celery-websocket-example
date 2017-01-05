from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('customers.urls')),
    url(r'^', include('loans.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='index'),
]
