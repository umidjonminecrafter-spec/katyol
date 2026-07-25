from core.routing import path, create_router
from apps.purchasing import views

urlpatterns = [
    path("", views.list_purchases_view, methods=["GET"], summary="List purchase documents"),
    path("/list", views.list_purchases_view, methods=["GET"], summary="List purchase documents"),
    path("", views.create_purchase_view, methods=["POST"], status_code=201, summary="Create purchase document"),
    path("/create", views.create_purchase_view, methods=["POST"], status_code=201, summary="Create purchase document"),
    path("/{id}/status", views.update_purchase_status_view, methods=["PUT"], summary="Update purchase status"),
]

router = create_router(urlpatterns)
