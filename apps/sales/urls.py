from core.routing import path, create_router
from apps.sales import views

urlpatterns = [
    path("", views.list_sales_view, methods=["GET"], summary="List sales invoices"),
    path("/list", views.list_sales_view, methods=["GET"], summary="List sales invoices"),
    path("", views.create_sale_view, methods=["POST"], status_code=201, summary="Create sales invoice"),
    path("/create", views.create_sale_view, methods=["POST"], status_code=201, summary="Create sales invoice"),
]

router = create_router(urlpatterns)
