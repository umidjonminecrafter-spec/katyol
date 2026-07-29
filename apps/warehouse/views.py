from decimal import Decimal
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticated
from core.audit_helper import record_audit_log
from apps.warehouse.services import WarehouseService
from apps.warehouse.serializers import StockResponseSerializer, StockAdjustmentRequestSerializer

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_warehouse_stock_view(request):
    if request.method == 'GET':
        warehouse_id = request.query_params.get('warehouse_id')
        product_id = request.query_params.get('product_id')
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))

        items, total = WarehouseService.get_stocks(
            warehouse_id=warehouse_id, product_id=product_id, page=page, limit=limit
        )
        total_pages = (total + limit - 1) // limit if limit > 0 else 1

        response_items = StockResponseSerializer(items, many=True).data

        return Response({
            "success": True,
            "data": response_items,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages
            }
        })

    # POST (Create / Adjust stock entry)
    serializer = StockAdjustmentRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data

    delta = d.get('quantity_delta')
    if delta is None:
        delta = d.get('quantity', 0.0) or 0.0

    unit_cost = Decimal(str(d.get('unit_cost') or 0.0))
    movement_type = d.get('movement_type') or "ADJUSTMENT"

    stock = WarehouseService.adjust_stock(
        warehouse_id=d['warehouse_id'],
        product_id=d['product_id'],
        quantity_delta=Decimal(str(delta)),
        unit_cost=unit_cost,
        movement_type=movement_type,
        notes=d.get('notes')
    )

    record_audit_log(
        action="ADJUST_STOCK",
        entity_name="WAREHOUSE_STOCK",
        entity_id=stock.id,
        actor_id=request.user.id,
        new_values=d,
        request=request
    )

    return Response({"success": True, "data": StockResponseSerializer(stock).data}, status=201)
