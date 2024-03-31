from django.urls import path
from dashboard.views import mailing_view

app_name = 'mailing'

urlpatterns = [
    path('index/', mailing_view, name='index'),
]
