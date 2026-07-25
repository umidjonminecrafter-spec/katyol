from core.routing import path, create_router
from apps.finance import views

urlpatterns = [
    path("/transactions", views.list_financial_transactions_view, methods=["GET"], summary="List financial transactions"),
    path("/transactions", views.create_financial_transaction_view, methods=["POST"], status_code=201, summary="Create financial transaction"),
]

router = create_router(urlpatterns)
