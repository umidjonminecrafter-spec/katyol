from typing import Optional
from fastapi import Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.production.services import ProductionService
from apps.production.schemas import ProductionBatchCreate, ProductionBatchUpdate, ProductionBatchResponse

async def list_production_batches_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await ProductionService.get_multi(db, page=page, limit=limit, status=status_filter)
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    response_items = []
    for b in items:
        resp = ProductionBatchResponse.model_validate(b)
        if b.boiler:
            resp.boiler_name = b.boiler.name
        response_items.append(resp)

    return {
        "success": True,
        "data": response_items,
        "pagination": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
    }

async def create_production_batch_view(
    request: Request,
    body: ProductionBatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER", "TECHNICIAN"]))
):
    batch = await ProductionService.create_batch(db, body.model_dump(), created_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name="PRODUCTION_BATCH",
        entity_id=batch.id,
        actor_id=current_user.id,
        new_values=body.model_dump(),
        request=request
    )
    resp = ProductionBatchResponse.model_validate(batch)
    if batch.boiler:
        resp.boiler_name = batch.boiler.name
    return {"success": True, "data": resp}

async def update_production_batch_view(
    id: str,
    request: Request,
    body: ProductionBatchUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER", "TECHNICIAN"]))
):
    batch = await ProductionService.update_batch(db, id, body.model_dump(exclude_unset=True), updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="UPDATE",
        entity_name="PRODUCTION_BATCH",
        entity_id=id,
        actor_id=current_user.id,
        new_values=body.model_dump(exclude_unset=True),
        request=request
    )
    resp = ProductionBatchResponse.model_validate(batch)
    if batch.boiler:
        resp.boiler_name = batch.boiler.name
    return {"success": True, "data": resp}
