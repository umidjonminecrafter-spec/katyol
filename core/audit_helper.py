import uuid
from typing import Any, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

async def record_audit_log(
    db: AsyncSession,
    action: str,
    entity_name: str,
    entity_id: str,
    actor_id: Optional[str] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None
):
    from apps.audit.models import AuditLog
    
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

    log_entry = AuditLog(
        id=str(uuid.uuid4()),
        actor_id=actor_id,
        action=action,
        entity_name=entity_name,
        entity_id=str(entity_id),
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log_entry)
    await db.flush()
