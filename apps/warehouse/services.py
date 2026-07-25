from typing import List, Tuple, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from apps.warehouse.models import WarehouseStock, StockMovement

class WarehouseService:
    @staticmethod
    async def get_stocks(
        db: AsyncSession,
        warehouse_id: Optional[str] = None,
        product_id: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[WarehouseStock], int]:
        query = select(WarehouseStock)
        count_query = select(func.count()).select_from(WarehouseStock)

        if warehouse_id:
            query = query.where(WarehouseStock.warehouse_id == warehouse_id)
            count_query = count_query.where(WarehouseStock.warehouse_id == warehouse_id)

        if product_id:
            query = query.where(WarehouseStock.product_id == product_id)
            count_query = count_query.where(WarehouseStock.product_id == product_id)

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        skip = (page - 1) * limit
        query = query.order_by(WarehouseStock.updated_at.desc()).offset(skip).limit(limit)
        res = await db.execute(query)
        items = list(res.scalars().all())

        return items, total

    @staticmethod
    async def record_receipt(
        db: AsyncSession,
        warehouse_id: str,
        product_id: str,
        quantity: Decimal,
        unit_cost: Decimal,
        reference_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> WarehouseStock:
        res = await db.execute(
            select(WarehouseStock).where(
                WarehouseStock.warehouse_id == warehouse_id,
                WarehouseStock.product_id == product_id
            )
        )
        stock = res.scalars().first()

        if not stock:
            stock = WarehouseStock(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=quantity,
                reserved_quantity=Decimal("0.000"),
                avg_unit_cost=unit_cost
            )
            db.add(stock)
        else:
            old_total = stock.quantity * stock.avg_unit_cost
            new_addition = quantity * unit_cost
            new_qty = stock.quantity + quantity
            if new_qty > 0:
                stock.avg_unit_cost = (old_total + new_addition) / new_qty
            stock.quantity = new_qty

        movement = StockMovement(
            movement_type="PURCHASE_RECEIPT",
            warehouse_id=warehouse_id,
            product_id=product_id,
            quantity=quantity,
            reference_id=reference_id,
            notes=notes
        )
        db.add(movement)
        await db.flush()
        return stock
