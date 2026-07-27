from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticated, require_roles
from core.audit_helper import record_audit_log
from apps.finance.models import FinancialTransaction
from apps.finance.serializers import TransactionCreateSerializer, TransactionResponseSerializer

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def financial_transactions_view(request):
    if request.method == 'GET':
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))

        qs = FinancialTransaction.objects.all().order_by('-created_at')
        total = qs.count()
        skip = (page - 1) * limit
        items = list(qs[skip:skip + limit])

        resp = TransactionResponseSerializer(items, many=True).data
        return Response({"success": True, "data": resp})

    # POST (create)
    if request.user.role not in ['ADMIN', 'ACCOUNTANT']:
        return Response({"success": False, "error_code": "FORBIDDEN", "message": "Ruxsat etilmagan"}, status=403)

    serializer = TransactionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    body_data = serializer.validated_data

    tx = FinancialTransaction.objects.create(
        transaction_number=body_data["transaction_number"],
        type=body_data["type"],
        expense_type_id=body_data.get("expense_type_id"),
        amount=body_data["amount"],
        currency=body_data["currency"],
        reference_id=body_data.get("reference_id"),
        transaction_date=body_data["transaction_date"],
        notes=body_data.get("notes"),
        created_by_id=request.user.id
    )

    record_audit_log(
        action="CREATE",
        entity_name="FINANCIAL_TRANSACTION",
        entity_id=tx.id,
        actor_id=request.user.id,
        new_values=body_data,
        request=request
    )
    return Response({"success": True, "data": TransactionResponseSerializer(tx).data}, status=201)
