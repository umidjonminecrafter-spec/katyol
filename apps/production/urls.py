from django.urls import re_path
from apps.production import views

urlpatterns = [
    re_path(r'^/batches/?$', views.production_batches_list_create_view),
    re_path(r'^/batches/(?P<id>[^/]+)/?$', views.update_production_batch_view),
]
