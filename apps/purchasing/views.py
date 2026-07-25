from typing import Optional
from fastapi import Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.purchasing.services import PurchaseService
from apps.purchasing.schemas import PurchaseCreate, PurchaseUpdateStatus, PurchaseResponse, PurchaseItemResponse

async def list_purchases_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await PurchaseService.get_multi(db, page=page, limit=limit, status=status_filter)
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    response_items = []
    for p in items:
        resp = PurchaseResponse.model_validate(p)
        if p.supplier:
            resp.supplier_name = p.supplier.name
        if p.warehouse:
            resp.warehouse_name = p.warehouse.name
        
        items_resp = []
        for item in p.items:
            i_resp = PurchaseItemResponse.model_validate(item)
            if item.product:
                i_resp.product_code = item.product.code
                i_resp.product_name = item.product.name
            items_resp.append(i_resp)
        resp.items = items_resp
        response_items.append(resp)

    return {
        "success": True,
        "data": response_items,
        "pagination": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
    }

async def create_purchase_view(
    request: Request,
    body: PurchaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER", "ACCOUNTANT", "WAREHOUSE_KEEPER"]))
):
    p = await PurchaseService.create_purchase(db, body.model_dump(), created_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name="PURCHASE",
        entity_id=p.id,
        actor_id=current_user.id,
        new_values=body.model_dump(),
        request=request
    )
    resp = PurchaseResponse.model_validate(p)
    if p.supplier:
        resp.supplier_name = p.supplier.name
    if p.warehouse:
        resp.warehouse_name = p.warehouse.name
    return {"success": True, "data": resp}

async def update_purchase_status_view(
    id: str,
    request: Request,
    body: PurchaseUpdateStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER", "ACCOUNTANT", "WAREHOUSE_KEEPER"]))
):
    p = await PurchaseService.update_status(db, id, body.status, updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="UPDATE_STATUS",
        entity_name="PURCHASE",
        entity_id=id,
        actor_id=current_user.id,
        new_values={"status": body.status},
        request=request
    )
    resp = PurchaseResponse.model_validate(p)
    if p.supplier:
        resp.supplier_name = p.supplier.name
    if p.warehouse:
        resp.warehouse_name = p.warehouse.name
    return {"success": True, "data": resp}
