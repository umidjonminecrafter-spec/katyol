from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.exceptions import CustomAppException
from core.base_repository import BaseRepository
from core.safe_delete import SafeDeleteService
from apps.products.models import Product

class ProductService:
    @staticmethod
    async def get_multi(
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category_id: Optional[str] = None,
        product_type: Optional[str] = None,
        status: str = "ACTIVE"
    ) -> Tuple[List[Product], int]:
        query = select(Product)
        count_query = select(func.count()).select_from(Product)

        if status:
            query = query.where(Product.status == status)
            count_query = count_query.where(Product.status == status)

        if category_id:
            query = query.where(Product.category_id == category_id)
            count_query = count_query.where(Product.category_id == category_id)

        if product_type:
            query = query.where(Product.type == product_type)
            count_query = count_query.where(Product.type == product_type)

        if search:
            search_pattern = f"%{search}%"
            query = query.where((Product.name.ilike(search_pattern)) | (Product.code.ilike(search_pattern)))
            count_query = count_query.where((Product.name.ilike(search_pattern)) | (Product.code.ilike(search_pattern)))

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        skip = (page - 1) * limit
        query = query.order_by(Product.created_at.desc()).offset(skip).limit(limit)
        res = await db.execute(query)
        items = list(res.scalars().all())

        return items, total

    @staticmethod
    async def create(db: AsyncSession, data: dict, created_by_id: str) -> Product:
        code = data.get("code")
        existing = await db.execute(select(Product).where(Product.code == code))
        if existing.scalars().first():
            raise CustomAppException(
                message="Ushbu mahsulot kodi tizimda allaqachon mavjud",
                error_code="VALIDATION_ERROR",
                errors=[{"field": "code", "message": "Ushbu mahsulot kodi tizimda allaqachon mavjud"}]
            )
        
        repo = BaseRepository(Product)
        return await repo.create(db, data, created_by_id=created_by_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: str) -> Product:
        repo = BaseRepository(Product)
        item = await repo.get_by_id(db, product_id)
        if not item:
            raise CustomAppException(message="Mahsulot topilmadi", status_code=404)
        return item

    @staticmethod
    async def update(db: AsyncSession, product_id: str, data: dict, updated_by_id: str) -> Product:
        repo = BaseRepository(Product)
        item = await repo.get_by_id(db, product_id)
        if not item:
            raise CustomAppException(message="Mahsulot topilmadi", status_code=404)
        return await repo.update(db, item, data, updated_by_id=updated_by_id)

    @staticmethod
    async def delete(db: AsyncSession, product_id: str) -> bool:
        repo = BaseRepository(Product)
        item = await repo.get_by_id(db, product_id)
        if not item:
            raise CustomAppException(message="Mahsulot topilmadi", status_code=404)
        
        await SafeDeleteService.check_entity_references(db, "products", product_id)
        return await repo.hard_delete(db, product_id)
