from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.exceptions import EntityInUseException

class SafeDeleteService:
    @staticmethod
    async def check_entity_references(db: AsyncSession, entity_key: str, entity_id: str):
        from apps.products.models import Product, RecipeItem
        from apps.purchasing.models import PurchaseItem
        from apps.sales.models import Sale
        from apps.warehouse.models import WarehouseStock

        total_references = 0
        entity_name_uz = "Ushbu resurs"

        if entity_key == "product-categories":
            res = await db.execute(select(func.count()).select_from(Product).where(Product.category_id == entity_id, Product.status != "ARCHIVED"))
            total_references = res.scalar() or 0
            entity_name_uz = "kategoriya"

        elif entity_key == "units":
            res = await db.execute(select(func.count()).select_from(Product).where(Product.unit_id == entity_id, Product.status != "ARCHIVED"))
            total_references = res.scalar() or 0
            entity_name_uz = "o'lchov birligi"

        elif entity_key == "material-types":
            res = await db.execute(select(func.count()).select_from(Product).where(Product.material_type_id == entity_id, Product.status != "ARCHIVED"))
            total_references = res.scalar() or 0
            entity_name_uz = "material turi"

        elif entity_key == "suppliers":
            res = await db.execute(select(func.count()).select_from(Product).where(Product.supplier_id == entity_id, Product.status != "ARCHIVED"))
            p_count = res.scalar() or 0
            res2 = await db.execute(select(func.count()).select_from(PurchaseItem).where(PurchaseItem.product_id == entity_id))
            total_references = p_count + (res2.scalar() or 0)
            entity_name_uz = "yetkazib beruvchi"

        elif entity_key == "customers":
            res = await db.execute(select(func.count()).select_from(Sale).where(Sale.customer_id == entity_id))
            total_references = res.scalar() or 0
            entity_name_uz = "mijoz"

        elif entity_key == "warehouses":
            res = await db.execute(select(func.count()).select_from(WarehouseStock).where(WarehouseStock.warehouse_id == entity_id))
            total_references = res.scalar() or 0
            entity_name_uz = "ombor"

        elif entity_key == "products":
            res = await db.execute(select(func.count()).select_from(RecipeItem).where(RecipeItem.material_product_id == entity_id))
            r_count = res.scalar() or 0
            res2 = await db.execute(select(func.count()).select_from(PurchaseItem).where(PurchaseItem.product_id == entity_id))
            pur_count = res2.scalar() or 0
            res3 = await db.execute(select(func.count()).select_from(Sale).where(Sale.product_id == entity_id))
            sale_count = res3.scalar() or 0
            total_references = r_count + pur_count + sale_count
            entity_name_uz = "mahsulot"

        if total_references > 0:
            raise EntityInUseException(
                message=f"Ushbu {entity_name_uz} {total_references} ta ob'ektga biriktirilgan. O'chirish taqiqlangan.",
                reference_count=total_references,
                can_archive=True
            )
