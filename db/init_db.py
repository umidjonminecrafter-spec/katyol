import asyncio
from sqlalchemy.future import select
from core.config import settings
from core.database import AsyncSessionLocal, engine, Base
from core.security import get_password_hash
from apps.accounts.models import User, Organization, Branch
from apps.master_data.models import ProductCategory, Unit, Warehouse

async def init_db(force_drop=False):
    async with engine.begin() as conn:
        if force_drop:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 1. Default Organization and Branch
        org = Organization(name="Kotyol Group", description="Asosiy Isitish Kotyollari Tashkiloti")
        session.add(org)
        await session.flush()

        branch = Branch(
            organization_id=org.id,
            name="Asosiy filial",
            code="MAIN-BRANCH",
            address="Toshkent shahri",
            phone="+998901234567"
        )
        session.add(branch)
        await session.flush()

        # 2. Superadmin user
        user_res = await session.execute(select(User).where(User.username == settings.SUPERADMIN_USERNAME))
        admin_user = user_res.scalars().first()
        if not admin_user:
            admin_user = User(
                username=settings.SUPERADMIN_USERNAME,
                full_name="Alex Vance",
                hashed_password=get_password_hash(settings.SUPERADMIN_PASSWORD),
                role="ADMIN",
                phone=settings.SUPERADMIN_USERNAME,
                department="Management",
                organization_name="Kotyol Group",
                branch_name="Asosiy filial",
                organization_id=org.id,
                branch_id=branch.id,
                status="ACTIVE"
            )
            session.add(admin_user)
            await session.flush()
            print(f"Superadmin user created: {settings.SUPERADMIN_USERNAME} / {settings.SUPERADMIN_PASSWORD}")

        # 3. Master Data
        cat_res = await session.execute(select(ProductCategory).where(ProductCategory.code == "CAT-BOILER"))
        cat = cat_res.scalars().first()
        if not cat:
            cat = ProductCategory(
                code="CAT-BOILER",
                name="Isitish Kotyollari",
                description="Kotyol mahsulotlari",
                organization_id=org.id,
                branch_id=branch.id
            )
            session.add(cat)

        unit_res = await session.execute(select(Unit).where(Unit.code == "UNIT-PCS"))
        unit = unit_res.scalars().first()
        if not unit:
            unit = Unit(
                code="UNIT-PCS",
                name="dona",
                symbol="dona",
                organization_id=org.id,
                branch_id=branch.id
            )
            session.add(unit)

        wh_res = await session.execute(select(Warehouse).where(Warehouse.code == "WH-MAIN"))
        wh = wh_res.scalars().first()
        if not wh:
            wh = Warehouse(
                code="WH-MAIN",
                name="Asosiy Ombor",
                location="Toshkent",
                organization_id=org.id,
                branch_id=branch.id
            )
            session.add(wh)

        await session.commit()
        print("Modular DB initialization & seed completed!")

if __name__ == "__main__":
    asyncio.run(init_db(force_drop=True))
