from core.routing import path, create_router
from apps.warehouse import views

urlpatterns = [
    path("/stock", views.get_warehouse_stock_view, methods=["GET"], summary="Get warehouse stock levels"),
]

router = create_router(urlpatterns)
