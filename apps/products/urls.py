from core.routing import path, create_router
from apps.products import views

urlpatterns = [
    path("", views.list_products_view, methods=["GET"], summary="List products catalog"),
    path("/list", views.list_products_view, methods=["GET"], summary="List products catalog"),
    path("", views.create_product_view, methods=["POST"], status_code=201, summary="Create a new product"),
    path("/create", views.create_product_view, methods=["POST"], status_code=201, summary="Create a new product"),
    path("/{id}", views.get_product_view, methods=["GET"], summary="Get product detail"),
    path("/{id}", views.update_product_view, methods=["PUT"], summary="Update product detail"),
    path("/{id}", views.delete_product_view, methods=["DELETE"], summary="Safe delete product"),
]

router = create_router(urlpatterns)
