from typing import Tuple, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.exceptions import CustomAppException
from core.base_repository import BaseRepository
from core.safe_delete import SafeDeleteService
from apps.master_data.models import (
    ProductCategory, MaterialType, Unit, Supplier, Customer,
    Warehouse, WarrantyType, CustomerType, ServiceType, Priority, OrderStatus, ExpenseType
)

MASTER_DATA_MODELS = {
    "product-categories": ProductCategory,
    "material-types": MaterialType,
    "units": Unit,
    "suppliers": Supplier,
    "customers": Customer,
    "warehouses": Warehouse,
    "warranty-types": WarrantyType,
    "customer-types": CustomerType,
    "service-types": ServiceType,
    "priorities": Priority,
    "order-statuses": OrderStatus,
    "expense-types": ExpenseType,
}

class MasterDataService:
    @staticmethod
    def get_model(entity_key: str):
        model = MASTER_DATA_MODELS.get(entity_key)
        if not model:
            raise CustomAppException(message=f"Entity key '{entity_key}' topilmadi", status_code=404)
        return model

    @classmethod
    async def get_multi(cls, db: AsyncSession, entity_key: str, include_archived: bool = False):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        return await repo.get_multi(db, skip=0, limit=1000, include_archived=include_archived)

    @classmethod
    async def create(cls, db: AsyncSession, entity_key: str, data: dict, created_by_id: str):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        if "code" in data:
            existing = await db.execute(select(model).where(model.code == data["code"]))
            if existing.scalars().first():
                raise CustomAppException(message=f"'{data['code']}' kodli master data allaqachon mavjud", error_code="DUPLICATE_CODE")
        return await repo.create(db, data, created_by_id=created_by_id)

    @classmethod
    async def update(cls, db: AsyncSession, entity_key: str, item_id: str, data: dict, updated_by_id: str):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        item = await repo.get_by_id(db, item_id)
        if not item:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        return await repo.update(db, item, data, updated_by_id=updated_by_id)

    @classmethod
    async def archive(cls, db: AsyncSession, entity_key: str, item_id: str, updated_by_id: str):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        item = await repo.get_by_id(db, item_id)
        if not item:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        return await repo.soft_delete(db, item, updated_by_id=updated_by_id)

    @classmethod
    async def restore(cls, db: AsyncSession, entity_key: str, item_id: str, updated_by_id: str):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        item = await repo.get_by_id(db, item_id)
        if not item:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        item.status = "ACTIVE"
        item.is_active = True
        item.updated_by_id = updated_by_id
        await db.flush()
        return item

    @classmethod
    async def delete(cls, db: AsyncSession, entity_key: str, item_id: str):
        model = cls.get_model(entity_key)
        repo = BaseRepository(model)
        item = await repo.get_by_id(db, item_id)
        if not item:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        
        await SafeDeleteService.check_entity_references(db, entity_key, item_id)
        return await repo.hard_delete(db, item_id)
