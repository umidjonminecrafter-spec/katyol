from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticated
from apps.warehouse.services import WarehouseService
from apps.warehouse.serializers import StockResponseSerializer

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_warehouse_stock_view(request):
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
