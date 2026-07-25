from core.routing import path, create_router
from apps.accounts import views

urlpatterns = [
    path("/login", views.login_view, methods=["POST"], summary="Authenticate user"),
    path("/register", views.register_view, methods=["POST"], summary="Register new organization user"),
    path("/employees", views.list_employees_view, methods=["GET"], summary="List branch employees"),
    path("/employees", views.create_employee_view, methods=["POST"], summary="Create new branch employee"),
    path("/refresh", views.refresh_token_view, methods=["POST"], summary="Refresh access token"),
    path("/me", views.get_me_view, methods=["GET"], summary="Get current user profile"),
    path("/branches", views.list_branches_view, methods=["GET"], summary="List organization branches"),
    path("/branches", views.create_branch_view, methods=["POST"], summary="Create organization branch"),
    path("/branches/stats", views.get_branch_stats_view, methods=["GET"], summary="Get organization branch statistics"),
    path("/branches/{id}", views.update_branch_view, methods=["PUT"], summary="Update branch"),
    path("/branches/{id}", views.delete_branch_view, methods=["DELETE"], summary="Delete branch"),
    path("/positions", views.list_positions_view, methods=["GET"], summary="List positions"),
    path("/positions", views.create_position_view, methods=["POST"], summary="Create position"),
    path("/positions/{id}", views.update_position_view, methods=["PUT"], summary="Update position"),
    path("/positions/{id}", views.delete_position_view, methods=["DELETE"], summary="Delete position"),
]

router = create_router(urlpatterns)
