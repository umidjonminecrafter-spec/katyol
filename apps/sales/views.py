from fastapi import Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.sales.services import SalesService
from apps.sales.schemas import SaleCreate, SaleResponse

async def list_sales_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await SalesService.get_multi(db, page=page, limit=limit)
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    response_items = []
    for s in items:
        resp = SaleResponse.model_validate(s)
        if s.customer:
            resp.customer_name = s.customer.name
        response_items.append(resp)

    return {
        "success": True,
        "data": response_items,
        "pagination": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
    }

async def create_sale_view(
    request: Request,
    body: SaleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER", "ACCOUNTANT"]))
):
    sale = await SalesService.create_sale(db, body.model_dump(), created_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name="SALE",
        entity_id=sale.id,
        actor_id=current_user.id,
        new_values=body.model_dump(),
        request=request
    )
    resp = SaleResponse.model_validate(sale)
    if sale.customer:
        resp.customer_name = sale.customer.name
    return {"success": True, "data": resp}
