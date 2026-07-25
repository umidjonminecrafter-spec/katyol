from core.routing import path, create_router
from apps.dashboard import views

urlpatterns = [
    path("/summary", views.get_summary_view, methods=["GET"], summary="Get executive dashboard summary KPIs"),
    path("/charts", views.get_charts_view, methods=["GET"], summary="Get dashboard analytics charts"),
]

router = create_router(urlpatterns)
