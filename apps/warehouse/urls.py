from django.urls import re_path
from apps.warehouse import views

urlpatterns = [
    re_path(r'^/stock/?$', views.get_warehouse_stock_view),
]
