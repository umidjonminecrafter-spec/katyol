from django.urls import re_path
from apps.finance import views

urlpatterns = [
    re_path(r'^/transactions/?$', views.financial_transactions_view),
]
