from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.master_data.models import Company
from apps.master_data.services import MasterDataService
from apps.master_data.schemas import MasterDataCreate, MasterDataUpdate, MasterDataResponse, CompanyUpdate, CompanyResponse

async def list_master_data_view(
    entity_key: str,
    include_archived: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await MasterDataService.get_multi(db, entity_key, include_archived=include_archived)
    resp = [MasterDataResponse.model_validate(item) for item in items]
    return {"success": True, "data": resp}

async def create_master_data_view(
    entity_key: str,
    request: Request,
    body: MasterDataCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    item = await MasterDataService.create(db, entity_key, body.model_dump(exclude_unset=True), created_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name=entity_key.upper(),
        entity_id=item.id,
        actor_id=current_user.id,
        new_values=body.model_dump(exclude_unset=True),
        request=request
    )
    return {"success": True, "data": MasterDataResponse.model_validate(item)}

async def update_master_data_view(
    entity_key: str,
    id: str,
    request: Request,
    body: MasterDataUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    item = await MasterDataService.update(db, entity_key, id, body.model_dump(exclude_unset=True), updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="UPDATE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=current_user.id,
        new_values=body.model_dump(exclude_unset=True),
        request=request
    )
    return {"success": True, "data": MasterDataResponse.model_validate(item)}

async def archive_master_data_view(
    entity_key: str,
    id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    item = await MasterDataService.archive(db, entity_key, id, updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="ARCHIVE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=current_user.id,
        request=request
    )
    return {"success": True, "data": MasterDataResponse.model_validate(item)}

async def restore_master_data_view(
    entity_key: str,
    id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    item = await MasterDataService.restore(db, entity_key, id, updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="RESTORE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=current_user.id,
        request=request
    )
    return {"success": True, "data": MasterDataResponse.model_validate(item)}

async def delete_master_data_view(
    entity_key: str,
    id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    await MasterDataService.delete(db, entity_key, id)
    await record_audit_log(
        db=db,
        action="DELETE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=current_user.id,
        request=request
    )
    return {"success": True, "data": {"id": id, "deleted": True}}

async def get_company_profile_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Company))
    company = result.scalars().first()
    if not company:
        company = Company(
            name="Kotyol Manufacturing",
            phone="+998 (90) 123-45-67",
            website="https://kotyol.uz",
            address="Toshkent sh., Chilonzor tumani, 5-daha",
            description="Yuqori sifatli isitish kotyollari ishlab chiqarish zavodi.",
            currency="USD",
            timezone="Asia/Tashkent (UTC+5)",
            date_format="YYYY-MM-DD"
        )
        db.add(company)
        await db.flush()
        await db.commit()
    return {"success": True, "data": CompanyResponse.model_validate(company)}

async def update_company_profile_view(
    request: Request,
    body: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    result = await db.execute(select(Company))
    company = result.scalars().first()
    if not company:
        company = Company(name="Kotyol Manufacturing")
        db.add(company)
        await db.flush()
    
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)
    
    await db.flush()
    await db.commit()
    
    await record_audit_log(
        db=db,
        action="UPDATE",
        entity_name="COMPANY_PROFILE",
        entity_id=company.id,
        actor_id=current_user.id,
        new_values=update_data,
        request=request
    )
    return {"success": True, "data": CompanyResponse.model_validate(company)}
