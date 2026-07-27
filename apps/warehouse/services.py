from decimal import Decimal
from apps.warehouse.models import WarehouseStock, StockMovement

class WarehouseService:
    @staticmethod
    def get_stocks(
        warehouse_id: str = None,
        product_id: str = None,
        page: int = 1,
        limit: int = 20
    ):
        qs = WarehouseStock.objects.all()

        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)

        if product_id:
            qs = qs.filter(product_id=product_id)

        total = qs.count()

        skip = (page - 1) * limit
        items = list(qs.order_by('-updated_at')[skip:skip + limit])

        return items, total

    @staticmethod
    def record_receipt(
        warehouse_id: str,
        product_id: str,
        quantity: Decimal,
        unit_cost: Decimal,
        reference_id: str = None,
        notes: str = None
    ) -> WarehouseStock:
        stock = WarehouseStock.objects.filter(warehouse_id=warehouse_id, product_id=product_id).first()

        if not stock:
            stock = WarehouseStock.objects.create(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=quantity,
                reserved_quantity=Decimal("0.000"),
                avg_unit_cost=unit_cost
            )
        else:
            old_total = stock.quantity * stock.avg_unit_cost
            new_addition = quantity * unit_cost
            new_qty = stock.quantity + quantity
            if new_qty > 0:
                stock.avg_unit_cost = (old_total + new_addition) / new_qty
            stock.quantity = new_qty
            stock.save()

        StockMovement.objects.create(
            movement_type="PURCHASE_RECEIPT",
            warehouse_id=warehouse_id,
            product_id=product_id,
            quantity=quantity,
            reference_id=reference_id,
            notes=notes
        )
        return stock
