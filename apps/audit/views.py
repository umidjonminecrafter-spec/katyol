from typing import Optional
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.database import get_db
from core.dependencies import RequireRole
from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.audit.schemas import AuditLogResponse

async def list_audit_logs_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    action: Optional[str] = None,
    entity_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    query = select(AuditLog)
    count_query = select(func.count()).select_from(AuditLog)

    if action:
        query = query.where(AuditLog.action == action)
        count_query = count_query.where(AuditLog.action == action)

    if entity_name:
        query = query.where(AuditLog.entity_name == entity_name)
        count_query = count_query.where(AuditLog.entity_name == entity_name)

    total_res = await db.execute(count_query)
    total = total_res.scalar() or 0

    skip = (page - 1) * limit
    query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
    res = await db.execute(query)
    items = list(res.scalars().all())

    resp = [AuditLogResponse.model_validate(item) for item in items]
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    return {
        "success": True,
        "data": resp,
        "pagination": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
    }
