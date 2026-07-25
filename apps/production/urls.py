from core.routing import path, create_router
from apps.production import views

urlpatterns = [
    path("/batches", views.list_production_batches_view, methods=["GET"], summary="List production batches"),
    path("/batches", views.create_production_batch_view, methods=["POST"], status_code=201, summary="Create production batch"),
    path("/batches/{id}", views.update_production_batch_view, methods=["PUT"], summary="Update production batch"),
]

router = create_router(urlpatterns)
