from decimal import Decimal
from core.exceptions import CustomAppException
from apps.sales.models import Sale

class SalesService:
    @staticmethod
    def create_sale(data: dict, created_by_id: str) -> Sale:
        inv_num = data.get("invoice_number")
        if Sale.objects.filter(invoice_number=inv_num).exists():
            raise CustomAppException(message=f"'{inv_num}' raqamli sotuv hisobi allaqachon mavjud", error_code="DUPLICATE_INVOICE_NUMBER")

        qty = Decimal(str(data["quantity"]))
        unit_price = Decimal(str(data["unit_price"]))
        subtotal = qty * unit_price
        disc = Decimal(str(data.get("discount_amount", 0)))
        tax = Decimal(str(data.get("tax_amount", 0)))
        total_amount = subtotal - disc + tax

        sale = Sale.objects.create(
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
        return sale

    @staticmethod
    def update_status(sale_id: str, data: dict, updated_by_id: str) -> Sale:
        try:
            sale = Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            raise CustomAppException(message="Sotuv hujjati topilmadi", status_code=404)

        if "payment_status" in data and data["payment_status"]:
            sale.payment_status = data["payment_status"]
        if "delivery_status" in data and data["delivery_status"]:
            sale.delivery_status = data["delivery_status"]

        sale.updated_by_id = updated_by_id
        sale.save()
        return sale

    @staticmethod
    def get_multi(
        page: int = 1,
        limit: int = 20
    ):
        qs = Sale.objects.all()
        total = qs.count()

        skip = (page - 1) * limit
        items = list(qs.order_by('-created_at')[skip:skip + limit])

        return items, total
