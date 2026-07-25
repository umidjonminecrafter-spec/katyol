from typing import Generic, TypeVar, Type, Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete
from core.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: str) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        include_archived: bool = False,
        status: Optional[str] = None,
        organization_id: Optional[str] = None,
        branch_id: Optional[str] = None
    ) -> Tuple[List[ModelType], int]:
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        if not include_archived:
            query = query.where(self.model.status != "ARCHIVED")
            count_query = count_query.where(self.model.status != "ARCHIVED")

        if status:
            query = query.where(self.model.status == status)
            count_query = count_query.where(self.model.status == status)

        if organization_id:
            query = query.where(self.model.organization_id == organization_id)
            count_query = count_query.where(self.model.organization_id == organization_id)

        if branch_id:
            query = query.where(self.model.branch_id == branch_id)
            count_query = count_query.where(self.model.branch_id == branch_id)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        items = list(result.scalars().all())

        return items, total

    async def create(
        self,
        db: AsyncSession,
        obj_in_data: dict,
        created_by_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        branch_id: Optional[str] = None
    ) -> ModelType:
        if created_by_id and hasattr(self.model, "created_by_id"):
            obj_in_data["created_by_id"] = created_by_id
        if organization_id and hasattr(self.model, "organization_id"):
            obj_in_data["organization_id"] = organization_id
        if branch_id and hasattr(self.model, "branch_id"):
            obj_in_data["branch_id"] = branch_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in_data: dict, updated_by_id: Optional[str] = None) -> ModelType:
        if updated_by_id and hasattr(self.model, "updated_by_id"):
            obj_in_data["updated_by_id"] = updated_by_id
        for field, value in obj_in_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, db_obj: ModelType, updated_by_id: Optional[str] = None) -> ModelType:
        db_obj.status = "ARCHIVED"
        db_obj.is_active = False
        if updated_by_id and hasattr(self.model, "updated_by_id"):
            db_obj.updated_by_id = updated_by_id
        await db.flush()
        return db_obj

    async def hard_delete(self, db: AsyncSession, id: str) -> bool:
        await db.execute(delete(self.model).where(self.model.id == id))
        await db.flush()
        return True
