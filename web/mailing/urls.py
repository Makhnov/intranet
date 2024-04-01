from django.urls import path
from mailing.views import mailing_view

app_name = 'mailing'

urlpatterns = [
    path('', mailing_view, name='index'),
]
