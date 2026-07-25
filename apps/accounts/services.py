from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status, Request

from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from core.audit_helper import record_audit_log
from apps.accounts.models import User, Organization, Branch
from apps.accounts.schemas import RegisterRequest, UserCreate, LoginRequest, TokenData, UserInfo

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, body: RegisterRequest) -> User:
        existing_res = await db.execute(select(User).where(User.username == body.phone))
        if existing_res.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu telefon raqami bilan foydalanuvchi allaqachon mavjud"
            )
        
        # 1. Create Organization
        org = Organization(name=body.organization_name)
        db.add(org)
        await db.flush()

        # 2. Create default Branch
        branch = Branch(
            organization_id=org.id,
            name=body.branch_name,
            code="MAIN-BRANCH"
        )
        db.add(branch)
        await db.flush()

        # 3. Create Admin User linked to organization & branch
        user = User(
            username=body.phone,
            hashed_password=get_password_hash(body.password),
            full_name=body.full_name,
            phone=body.phone,
            role="ADMIN",
            organization_name=body.organization_name,
            branch_name=body.branch_name,
            organization_id=org.id,
            branch_id=branch.id,
            status="ACTIVE"
        )
        db.add(user)
        
        from apps.master_data.models import Company
        company_res = await db.execute(select(Company))
        company = company_res.scalars().first()
        if not company:
            company = Company(
                name=body.organization_name,
                phone=body.phone,
                currency=body.currency,
                timezone="Asia/Tashkent (UTC+5)",
                date_format="YYYY-MM-DD"
            )
            db.add(company)
        else:
            company.name = body.organization_name
            company.phone = body.phone
            company.currency = body.currency

        await db.flush()
        await db.commit()
        return user

    @staticmethod
    async def create_employee_user(db: AsyncSession, body: UserCreate, creator: User) -> User:
        existing_res = await db.execute(select(User).where(User.username == body.phone))
        if existing_res.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu telefon raqami bilan foydalanuvchi allaqachon mavjud"
            )
        
        user = User(
            username=body.phone,
            hashed_password=get_password_hash(body.password),
            full_name=body.full_name,
            phone=body.phone,
            role=body.role,
            position_id=body.position_id,
            department=body.department,
            organization_name=creator.organization_name,
            branch_name=creator.branch_name,
            organization_id=creator.organization_id,
            branch_id=creator.branch_id,
            status="ACTIVE"
        )
        db.add(user)
        await db.flush()
        await db.commit()
        return user

    @staticmethod
    async def list_employees(db: AsyncSession, creator: User):
        result = await db.execute(
            select(User).where(
                User.organization_name == creator.organization_name,
                User.branch_name == creator.branch_name
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def authenticate_user(db: AsyncSession, body: LoginRequest, request: Request) -> TokenData:
        result = await db.execute(select(User).where(User.username == body.username, User.status == "ACTIVE"))
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_FOUND"
            )
        
        if not verify_password(body.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Noto'g'ri parol"
            )

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id)

        await record_audit_log(
            db=db,
            action="LOGIN",
            entity_name="USER",
            entity_id=user.id,
            actor_id=user.id,
            request=request
        )

        user_info = UserInfo.model_validate(user)
        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_info
        )

    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token: str) -> str:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Yaroqsiz refresh token"
            )
        
        user_id = payload.get("sub")
        result = await db.execute(select(User).where(User.id == user_id, User.status == "ACTIVE"))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi topilmadi")

        return create_access_token(subject=user.id, role=user.role)
