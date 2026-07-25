from core.routing import path, create_router
from apps.audit import views

urlpatterns = [
    path("", views.list_audit_logs_view, methods=["GET"], summary="List audit logs history"),
    path("/logs", views.list_audit_logs_view, methods=["GET"], summary="List audit logs history"),
    path("/list", views.list_audit_logs_view, methods=["GET"], summary="List audit logs history"),
]

router = create_router(urlpatterns)
