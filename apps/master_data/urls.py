from django.urls import re_path
from apps.master_data import views

urlpatterns = [
    re_path(r'^/company/profile/?$', views.company_profile_view),
    re_path(r'^/(?P<entity_key>[^/]+)/create/?$', views.master_data_list_create_view),
    re_path(r'^/(?P<entity_key>[^/]+)/(?P<id>[^/]+)/archive/?$', views.archive_master_data_view),
    re_path(r'^/(?P<entity_key>[^/]+)/(?P<id>[^/]+)/restore/?$', views.restore_master_data_view),
    re_path(r'^/(?P<entity_key>[^/]+)/(?P<id>[^/]+)/?$', views.master_data_detail_view),
    re_path(r'^/(?P<entity_key>[^/]+)/?$', views.master_data_list_create_view),
]
