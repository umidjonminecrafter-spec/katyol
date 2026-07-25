from decimal import Decimal
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from core.exceptions import CustomAppException
from apps.sales.models import Sale

class SalesService:
    @staticmethod
    async def create_sale(db: AsyncSession, data: dict, created_by_id: str) -> Sale:
        inv_num = data.get("invoice_number")
        existing = await db.execute(select(Sale).where(Sale.invoice_number == inv_num))
        if existing.scalars().first():
            raise CustomAppException(message=f"'{inv_num}' raqamli sotuv hisobi allaqachon mavjud", error_code="DUPLICATE_INVOICE_NUMBER")

        qty = Decimal(str(data["quantity"]))
        unit_price = Decimal(str(data["unit_price"]))
        subtotal = qty * unit_price
        disc = Decimal(str(data.get("discount_amount", 0)))
        tax = Decimal(str(data.get("tax_amount", 0)))
        total_amount = subtotal - disc + tax

        sale = Sale(
            invoice_number=inv_num,
            customer_id=data["customer_id"],
            boiler_id=data.get("boiler_id"),
            product_id=data.get("product_id"),
            quantity=qty,
            unit_price=unit_price,
            subtotal=subtotal,
            discount_amount=disc,
            tax_amount=tax,
            total_amount=total_amount,
            exchange_rate_at_creation=Decimal(str(data.get("exchange_rate_at_creation", 1.0))),
            payment_status="UNPAID",
            delivery_status="PENDING",
            created_by_id=created_by_id
        )
        db.add(sale)
        await db.flush()
        return sale

    @staticmethod
    async def update_status(db: AsyncSession, sale_id: str, data: dict, updated_by_id: str) -> Sale:
        res = await db.execute(select(Sale).where(Sale.id == sale_id))
        sale = res.scalars().first()
        if not sale:
            raise CustomAppException(message="Sotuv hujjati topilmadi", status_code=404)

        if "payment_status" in data and data["payment_status"]:
            sale.payment_status = data["payment_status"]
        if "delivery_status" in data and data["delivery_status"]:
            sale.delivery_status = data["delivery_status"]

        sale.updated_by_id = updated_by_id
        await db.flush()
        return sale

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Sale], int]:
        query = select(Sale)
        count_query = select(func.count()).select_from(Sale)

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        skip = (page - 1) * limit
        query = query.order_by(Sale.created_at.desc()).offset(skip).limit(limit)
        res = await db.execute(query)
        items = list(res.scalars().all())

        return items, total
