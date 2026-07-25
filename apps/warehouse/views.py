from typing import Optional
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user
from apps.accounts.models import User
from apps.warehouse.services import WarehouseService
from apps.warehouse.schemas import StockResponse

async def get_warehouse_stock_view(
    warehouse_id: Optional[str] = None,
    product_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await WarehouseService.get_stocks(
        db, warehouse_id=warehouse_id, product_id=product_id, page=page, limit=limit
    )
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    
    response_items = []
    for item in items:
        resp = StockResponse.model_validate(item)
        resp.available_quantity = float(item.quantity - item.reserved_quantity)
        if item.warehouse:
            resp.warehouse_name = item.warehouse.name
        if item.product:
            resp.product_code = item.product.code
            resp.product_name = item.product.name
        response_items.append(resp)

    return {
        "success": True,
        "data": response_items,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    }
