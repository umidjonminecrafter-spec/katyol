from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.exceptions import CustomAppException
from apps.production.models import ProductionBatch

class ProductionService:
    @staticmethod
    async def create_batch(db: AsyncSession, data: dict, created_by_id: str) -> ProductionBatch:
        b_num = data.get("batch_number")
        existing = await db.execute(select(ProductionBatch).where(ProductionBatch.batch_number == b_num))
        if existing.scalars().first():
            raise CustomAppException(message=f"'{b_num}' raqamli ishlab chiqarish partiyasi allaqachon mavjud", error_code="DUPLICATE_BATCH_NUMBER")

        batch = ProductionBatch(
            batch_number=b_num,
            boiler_id=data["boiler_id"],
            target_quantity=data["target_quantity"],
            completed_quantity=0,
            defect_quantity=0,
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            status="PLANNED",
            created_by_id=created_by_id
        )
        db.add(batch)
        await db.flush()
        return batch

    @staticmethod
    async def update_batch(db: AsyncSession, batch_id: str, data: dict, updated_by_id: str) -> ProductionBatch:
        res = await db.execute(select(ProductionBatch).where(ProductionBatch.id == batch_id))
        batch = res.scalars().first()
        if not batch:
            raise CustomAppException(message="Ishlab chiqarish partiyasi topilmadi", status_code=404)

        for field, value in data.items():
            if value is not None and hasattr(batch, field):
                setattr(batch, field, value)

        batch.updated_by_id = updated_by_id
        await db.flush()
        return batch

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None
    ) -> Tuple[List[ProductionBatch], int]:
        query = select(ProductionBatch)
        count_query = select(func.count()).select_from(ProductionBatch)

        if status:
            query = query.where(ProductionBatch.status == status)
            count_query = count_query.where(ProductionBatch.status == status)

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        skip = (page - 1) * limit
        query = query.order_by(ProductionBatch.created_at.desc()).offset(skip).limit(limit)
        res = await db.execute(query)
        items = list(res.scalars().all())

        return items, total
