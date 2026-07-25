from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user
from apps.accounts.models import User
from apps.accounts.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, UserProfileResponse, UserInfo, RegisterRequest, UserCreate
from apps.accounts.services import AuthService

async def register_view(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthService.register_user(db, body)
    return {"success": True, "data": UserInfo.model_validate(user)}

async def list_employees_view(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = await AuthService.list_employees(db, current_user)
    return {"success": True, "data": [UserInfo.model_validate(u) for u in users]}

async def create_employee_view(body: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await AuthService.create_employee_user(db, body, current_user)
    return {"success": True, "data": UserInfo.model_validate(user)}

async def login_view(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    token_data = await AuthService.authenticate_user(db, body, request)
    return LoginResponse(success=True, data=token_data)

async def refresh_token_view(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    access_token = await AuthService.refresh_access_token(db, body.refresh_token)
    return RefreshResponse(access_token=access_token, token_type="bearer")

async def get_me_view(current_user: User = Depends(get_current_user)):
    user_info = UserInfo.model_validate(current_user)
    
    permissions = []
    if current_user.position and current_user.position.permissions:
        import json
        try:
            permissions = json.loads(current_user.position.permissions)
        except Exception:
            permissions = current_user.position.permissions.split(",")

    if not permissions:
        if current_user.role in ["ADMIN", "SUPER_ADMIN"]:
            permissions = ["*"]
        elif current_user.role == "PRODUCTION_OPERATOR":
            permissions = ["PRODUCTION_VIEW", "PRODUCTION_EDIT"]
        elif current_user.role == "WAREHOUSE_KEEPER":
            permissions = ["WAREHOUSE_VIEW", "WAREHOUSE_EDIT"]
        else:
            permissions = ["PRODUCTION_VIEW", "WAREHOUSE_VIEW", "SALES_VIEW"]
    
    return UserProfileResponse(user=user_info, permissions=permissions)

# Branch management views
from apps.accounts.models import Branch, Organization
from apps.accounts.schemas import BranchCreate, BranchResponse
from sqlalchemy.future import select
from sqlalchemy import func

async def list_branches_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.organization_id:
        return {"success": True, "data": []}
    result = await db.execute(
        select(Branch).where(Branch.organization_id == current_user.organization_id)
    )
    branches = result.scalars().all()
    return {"success": True, "data": [BranchResponse.model_validate(b) for b in branches]}

async def create_branch_view(
    body: BranchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="Foydalanuvchi tashkilotga biriktirilmagan")
    
    branch = Branch(
        organization_id=current_user.organization_id,
        name=body.name,
        code=body.code,
        address=body.address,
        phone=body.phone
    )
    db.add(branch)
    await db.flush()
    await db.commit()
    return {"success": True, "data": BranchResponse.model_validate(branch)}

async def update_branch_view(
    id: str,
    body: BranchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Branch).where(Branch.id == id, Branch.organization_id == current_user.organization_id)
    )
    branch = result.scalars().first()
    if not branch:
        raise HTTPException(status_code=404, detail="Filial topilmadi")
    
    branch.name = body.name
    branch.code = body.code
    branch.address = body.address
    branch.phone = body.phone
    
    await db.flush()
    await db.commit()
    return {"success": True, "data": BranchResponse.model_validate(branch)}

async def delete_branch_view(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Branch).where(Branch.id == id, Branch.organization_id == current_user.organization_id)
    )
    branch = result.scalars().first()
    if not branch:
        raise HTTPException(status_code=404, detail="Filial topilmadi")
    
    branch.status = "ARCHIVED"
    await db.flush()
    await db.commit()
    return {"success": True, "message": "Filial muvaffaqiyatli arxivlandi"}

async def get_branch_stats_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from apps.sales.models import Sale
    from apps.production.models import ProductionBatch
    from apps.warehouse.models import WarehouseStock

    if not current_user.organization_id:
        return {"success": True, "data": []}

    result = await db.execute(
        select(Branch).where(Branch.organization_id == current_user.organization_id, Branch.status == "ACTIVE")
    )
    branches = result.scalars().all()

    stats = []
    for b in branches:
        # Sum sales revenue
        sales_rev_res = await db.execute(
            select(func.sum(Sale.total_amount)).where(Sale.branch_id == b.id)
        )
        sales_rev = sales_rev_res.scalar() or 0

        # Sales count
        sales_cnt_res = await db.execute(
            select(func.count(Sale.id)).where(Sale.branch_id == b.id)
        )
        sales_cnt = sales_cnt_res.scalar() or 0

        # Production count
        prod_cnt_res = await db.execute(
            select(func.sum(ProductionBatch.completed_quantity)).where(ProductionBatch.branch_id == b.id)
        )
        prod_cnt = prod_cnt_res.scalar() or 0

        # Total warehouse stock
        stock_res = await db.execute(
            select(func.sum(WarehouseStock.quantity)).where(WarehouseStock.branch_id == b.id)
        )
        stock_cnt = stock_res.scalar() or 0

        stats.append({
            "id": b.id,
            "name": b.name,
            "code": b.code,
            "revenue": float(sales_rev),
            "salesCount": int(sales_cnt),
            "productionVolume": int(prod_cnt),
            "stockVolume": float(stock_cnt)
        })

    return {"success": True, "data": stats}

# Position CRUD views
from apps.accounts.models import Position
from apps.accounts.schemas import PositionCreate, PositionResponse

async def list_positions_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Position).where(Position.status != "ARCHIVED"))
    positions = result.scalars().all()
    return {"success": True, "data": [PositionResponse.model_validate(p) for p in positions]}

async def create_position_view(
    body: PositionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Auto-generate code from name
    code = body.name.strip().upper().replace(" ", "-")
    import uuid
    position = Position(
        code=f"{code}-{str(uuid.uuid4())[:4]}",
        name=body.name,
        description=body.description,
        permissions=body.permissions,
        status="ACTIVE"
    )
    db.add(position)
    await db.flush()
    await db.commit()
    return {"success": True, "data": PositionResponse.model_validate(position), "message": "Yangi lavozim muvaffaqiyatli saqlandi."}

async def update_position_view(
    id: str,
    body: PositionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Position).where(Position.id == id))
    position = result.scalars().first()
    if not position:
        raise HTTPException(status_code=404, detail="Lavozim topilmadi")
    
    position.name = body.name
    position.description = body.description
    if body.permissions is not None:
        position.permissions = body.permissions
    
    await db.flush()
    await db.commit()
    return {"success": True, "data": PositionResponse.model_validate(position), "message": "Lavozim muvaffaqiyatli tahrirlandi."}

async def delete_position_view(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Position).where(Position.id == id))
    position = result.scalars().first()
    if not position:
        raise HTTPException(status_code=404, detail="Lavozim topilmadi")
    
    position.status = "ARCHIVED"
    await db.flush()
    await db.commit()
    return {"success": True, "message": "Lavozim muvaffaqiyatli o'chirildi."}
