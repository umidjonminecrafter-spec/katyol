from decimal import Decimal
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.exceptions import CustomAppException
from apps.purchasing.models import Purchase, PurchaseItem
from apps.warehouse.services import WarehouseService

class PurchaseService:
    @staticmethod
    async def create_purchase(db: AsyncSession, data: dict, created_by_id: str) -> Purchase:
        items_data = data.pop("items", [])
        p_num = data.get("purchase_number")
        existing = await db.execute(select(Purchase).where(Purchase.purchase_number == p_num))
        if existing.scalars().first():
            raise CustomAppException(message=f"'{p_num}' raqamli xarid hujjati allaqachon mavjud", error_code="DUPLICATE_PURCHASE_NUMBER")

        subtotal = Decimal("0.00")
        purchase_items = []
        for item in items_data:
            tot = Decimal(str(item["quantity"])) * Decimal(str(item["unit_price"]))
            subtotal += tot
            purchase_items.append(
                PurchaseItem(
                    product_id=item["product_id"],
                    quantity=Decimal(str(item["quantity"])),
                    unit_price=Decimal(str(item["unit_price"])),
                    total_price=tot
                )
            )

        tax = Decimal(str(data.get("tax_amount", 0)))
        total_amount = subtotal + tax

        purchase = Purchase(
            purchase_number=p_num,
            supplier_id=data["supplier_id"],
            warehouse_id=data["warehouse_id"],
            invoice_number=data.get("invoice_number"),
            order_date=data["order_date"],
            subtotal=subtotal,
            tax_amount=tax,
            total_amount=total_amount,
            exchange_rate_at_creation=Decimal(str(data.get("exchange_rate_at_creation", 1.0))),
            status="DRAFT",
            created_by_id=created_by_id,
            items=purchase_items
        )
        db.add(purchase)
        await db.flush()
        return purchase

    @staticmethod
    async def update_status(db: AsyncSession, purchase_id: str, new_status: str, updated_by_id: str) -> Purchase:
        res = await db.execute(select(Purchase).where(Purchase.id == purchase_id))
        purchase = res.scalars().first()
        if not purchase:
            raise CustomAppException(message="Xarid hujjati topilmadi", status_code=404)

        if purchase.status == "RECEIVED":
            raise CustomAppException(message="Qabul qilingan xarid hujjati holatini o'zgartirib bo'lmaydi", error_code="PURCHASE_ALREADY_RECEIVED")

        if new_status == "RECEIVED":
            for item in purchase.items:
                await WarehouseService.record_receipt(
                    db=db,
                    warehouse_id=str(purchase.warehouse_id),
                    product_id=str(item.product_id),
                    quantity=Decimal(str(item.quantity)),
                    unit_cost=Decimal(str(item.unit_price)),
                    reference_id=str(purchase.id),
                    notes=f"Purchase receipt #{purchase.purchase_number}"
                )

        purchase.status = new_status
        purchase.updated_by_id = updated_by_id
        await db.flush()
        return purchase

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None
    ) -> Tuple[List[Purchase], int]:
        query = select(Purchase)
        count_query = select(func.count()).select_from(Purchase)

        if status:
            query = query.where(Purchase.status == status)
            count_query = count_query.where(Purchase.status == status)

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        skip = (page - 1) * limit
        query = query.order_by(Purchase.created_at.desc()).offset(skip).limit(limit)
        res = await db.execute(query)
        items = list(res.scalars().all())

        return items, total
