from typing import Optional
from fastapi import Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user, RequireRole
from core.audit_helper import record_audit_log
from apps.accounts.models import User
from apps.products.services import ProductService
from apps.products.schemas import ProductCreate, ProductUpdate, ProductResponse

async def list_products_view(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[str] = None,
    type: Optional[str] = None,
    status_filter: str = Query("ACTIVE", alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items, total = await ProductService.get_multi(
        db, page=page, limit=limit, search=search, category_id=category_id, product_type=type, status=status_filter
    )
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    
    response_items = []
    for item in items:
        resp = ProductResponse.model_validate(item)
        if item.category:
            resp.category_name = item.category.name
        if item.unit:
            resp.unit_name = item.unit.name
        if item.material_type:
            resp.material_type_name = item.material_type.name
        if item.supplier:
            resp.supplier_name = item.supplier.name
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

async def create_product_view(
    request: Request,
    body: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER"]))
):
    product = await ProductService.create(db, body.model_dump(), created_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="CREATE",
        entity_name="PRODUCT",
        entity_id=product.id,
        actor_id=current_user.id,
        new_values=body.model_dump(),
        request=request
    )
    resp = ProductResponse.model_validate(product)
    if product.category:
        resp.category_name = product.category.name
    if product.unit:
        resp.unit_name = product.unit.name
    if product.material_type:
        resp.material_type_name = product.material_type.name
    if product.supplier:
        resp.supplier_name = product.supplier.name
    return {"success": True, "data": resp}

async def get_product_view(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = await ProductService.get_by_id(db, id)
    resp = ProductResponse.model_validate(product)
    if product.category:
        resp.category_name = product.category.name
    if product.unit:
        resp.unit_name = product.unit.name
    if product.material_type:
        resp.material_type_name = product.material_type.name
    if product.supplier:
        resp.supplier_name = product.supplier.name
    return {"success": True, "data": resp}

async def update_product_view(
    id: str,
    request: Request,
    body: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN", "MANAGER"]))
):
    old_product = await ProductService.get_by_id(db, id)
    old_values = {"name": old_product.name, "unit_price": float(old_product.unit_price)}
    updated = await ProductService.update(db, id, body.model_dump(exclude_unset=True), updated_by_id=current_user.id)
    await record_audit_log(
        db=db,
        action="UPDATE",
        entity_name="PRODUCT",
        entity_id=id,
        actor_id=current_user.id,
        old_values=old_values,
        new_values=body.model_dump(exclude_unset=True),
        request=request
    )
    resp = ProductResponse.model_validate(updated)
    if updated.category:
        resp.category_name = updated.category.name
    if updated.unit:
        resp.unit_name = updated.unit.name
    if updated.material_type:
        resp.material_type_name = updated.material_type.name
    if updated.supplier:
        resp.supplier_name = updated.supplier.name
    return {"success": True, "data": resp}

async def delete_product_view(
    id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequireRole(["ADMIN"]))
):
    await ProductService.delete(db, id)
    await record_audit_log(
        db=db,
        action="DELETE",
        entity_name="PRODUCT",
        entity_id=id,
        actor_id=current_user.id,
        request=request
    )
    return {"success": True, "data": {"id": id, "deleted": True}}
