from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticated
from core.audit_helper import record_audit_log
from apps.sales.services import SalesService
from apps.sales.serializers import SaleCreateSerializer, SaleResponseSerializer

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def sales_list_create_view(request):
    if request.method == 'GET':
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))

        items, total = SalesService.get_multi(page=page, limit=limit)
        total_pages = (total + limit - 1) // limit if limit > 0 else 1

        response_items = SaleResponseSerializer(items, many=True).data

        return Response({
            "success": True,
            "data": response_items,
            "pagination": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
        })

    # POST (create)
    if request.user.role not in ["ADMIN", "MANAGER", "ACCOUNTANT"]:
        return Response({"success": False, "error_code": "FORBIDDEN", "message": "Ruxsat etilmagan"}, status=403)

    serializer = SaleCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    body_data = serializer.validated_data

    sale = SalesService.create_sale(body_data, created_by_id=request.user.id)
    record_audit_log(
        action="CREATE",
        entity_name="SALE",
        entity_id=sale.id,
        actor_id=request.user.id,
        new_values=body_data,
        request=request
    )
    return Response({"success": True, "data": SaleResponseSerializer(sale).data}, status=201)
