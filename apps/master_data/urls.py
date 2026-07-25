from core.routing import path, create_router
from apps.master_data import views

urlpatterns = [
    path("/company/profile", views.get_company_profile_view, methods=["GET"], summary="Get company profile details"),
    path("/company/profile", views.update_company_profile_view, methods=["PUT"], summary="Update company profile details"),
    path("/{entity_key}", views.list_master_data_view, methods=["GET"], summary="List dynamic master data"),
    path("/{entity_key}", views.create_master_data_view, methods=["POST"], status_code=201, summary="Create master data entry"),
    path("/{entity_key}/{id}", views.update_master_data_view, methods=["PUT"], summary="Update master data entry"),
    path("/{entity_key}/{id}/archive", views.archive_master_data_view, methods=["POST"], summary="Archive master data entry"),
    path("/{entity_key}/{id}/restore", views.restore_master_data_view, methods=["POST"], summary="Restore archived master data entry"),
    path("/{entity_key}/{id}", views.delete_master_data_view, methods=["DELETE"], summary="Safe delete master data entry"),
]

router = create_router(urlpatterns)
