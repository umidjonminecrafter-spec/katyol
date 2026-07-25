from core.routing import path, create_router
from apps.files import views

urlpatterns = [
    path("/upload", views.upload_file_view, methods=["POST"], summary="Upload file asset"),
]

router = create_router(urlpatterns)
