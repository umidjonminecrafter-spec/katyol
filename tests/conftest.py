import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from main import app
from core.database import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestAsyncSessionLocal() as session:
        from core.security import get_password_hash
        from apps.accounts.models import User
        from apps.master_data.models import ProductCategory, Unit, Warehouse
        
        admin_user = User(
            username="admin@kotyol.uz",
            full_name="Alex Vance",
            hashed_password=get_password_hash("Password123!"),
            role="ADMIN",
            department="Management",
            status="ACTIVE"
        )
        cat = ProductCategory(code="CAT-BOILER", name="Isitish Kotyollari")
        unit = Unit(code="UNIT-PCS", name="dona")
        wh = Warehouse(code="WH-MAIN", name="Asosiy Ombor")
        
        session.add_all([admin_user, cat, unit, wh])
        await session.commit()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
