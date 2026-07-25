from typing import List
from fastapi import Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.finance.models import FinancialTransaction
from apps.finance.schemas import TransactionCreate, TransactionResponse

async def list_financial_transactions_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).offset((page - 1) * limit).limit(limit)
    res = await db.execute(query)
    items = list(res.scalars().all())
    resp = [TransactionResponse.model_validate(i) for i in items]
    return {"success": True, "data": resp}

async def create_financial_transaction_view(
    request: Request,
    body: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "ACCOUNTANT"]))
):
    tx = FinancialTransaction(
        transaction_number=body.transaction_number,
        type=body.type,
        expense_type_id=body.expense_type_id,
        amount=body.amount,
        currency=body.currency,
        reference_id=body.reference_id,
        transaction_date=body.transaction_date,
        notes=body.notes,
        created_by_id=current_user.id
    )
    db.add(tx)
    await db.flush()

    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name="FINANCIAL_TRANSACTION",
        entity_id=tx.id,
        actor_id=current_user.id,
        new_values=body.model_dump(),
        request=request
    )
    return {"success": True, "data": TransactionResponse.model_validate(tx)}
