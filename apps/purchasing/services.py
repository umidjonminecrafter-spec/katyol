from decimal import Decimal
from core.exceptions import CustomAppException
from apps.purchasing.models import Purchase, PurchaseItem
from apps.warehouse.services import WarehouseService

class PurchaseService:
    @staticmethod
    def create_purchase(data: dict, created_by_id: str) -> Purchase:
        items_data = data.pop("items", [])
        p_num = data.get("purchase_number")
        if Purchase.objects.filter(purchase_number=p_num).exists():
            raise CustomAppException(message=f"'{p_num}' raqamli xarid hujjati allaqachon mavjud", error_code="DUPLICATE_PURCHASE_NUMBER")

        subtotal = Decimal("0.00")
        purchase_items_to_create = []
        for item in items_data:
            tot = Decimal(str(item["quantity"])) * Decimal(str(item["unit_price"]))
            subtotal += tot
            purchase_items_to_create.append({
                "product_id": item["product_id"],
                "quantity": Decimal(str(item["quantity"])),
                "unit_price": Decimal(str(item["unit_price"])),
                "total_price": tot
            })

        tax = Decimal(str(data.get("tax_amount", 0)))
        total_amount = subtotal + tax

        purchase = Purchase.objects.create(
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
            created_by_id=created_by_id
        )

        for item_dict in purchase_items_to_create:
            PurchaseItem.objects.create(purchase=purchase, **item_dict)

        return purchase

    @staticmethod
    def update_status(purchase_id: str, new_status: str, updated_by_id: str) -> Purchase:
        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except Purchase.DoesNotExist:
            raise CustomAppException(message="Xarid hujjati topilmadi", status_code=404)

        if purchase.status == "RECEIVED":
            raise CustomAppException(message="Qabul qilingan xarid hujjati holatini o'zgartirib bo'lmaydi", error_code="PURCHASE_ALREADY_RECEIVED")

        if new_status == "RECEIVED":
            for item in purchase.items.all():
                WarehouseService.record_receipt(
                    warehouse_id=str(purchase.warehouse_id),
                    product_id=str(item.product_id),
                    quantity=Decimal(str(item.quantity)),
                    unit_cost=Decimal(str(item.unit_price)),
                    reference_id=str(purchase.id),
                    notes=f"Purchase receipt #{purchase.purchase_number}"
                )

        purchase.status = new_status
        purchase.updated_by_id = updated_by_id
        purchase.save()
        return purchase

    @staticmethod
    def get_multi(
        page: int = 1,
        limit: int = 20,
        status: str = None
    ):
        qs = Purchase.objects.all()

        if status:
            qs = qs.filter(status=status)

        total = qs.count()

        skip = (page - 1) * limit
        items = list(qs.order_by('-created_at')[skip:skip + limit])

        return items, total
