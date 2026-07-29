import uuid
import datetime
from decimal import Decimal
from core.exceptions import CustomAppException
from apps.sales.models import Sale
from apps.master_data.models import Customer
from apps.products.models import Boiler, Product

class SalesService:
    @staticmethod
    def create_sale(data: dict, created_by_id: str) -> Sale:
        inv_num = (data.get("invoice_number") or "").strip()
        if not inv_num or inv_num in ["undefined", "null"]:
            inv_num = f"DOC-{datetime.date.today().year}-{str(uuid.uuid4())[:6].upper()}"

        if Sale.objects.filter(invoice_number=inv_num).exists():
            inv_num = f"DOC-{datetime.date.today().year}-{str(uuid.uuid4())[:6].upper()}"

        # Resolve Customer safely
        cust_id = (data.get("customer_id") or "").strip()
        customer = None
        if cust_id and cust_id not in ["undefined", "null"]:
            customer = Customer.objects.filter(id=cust_id).first()

        if not customer:
            customer = Customer.objects.first()

        if not customer:
            customer = Customer.objects.create(code="CUST-GEN", name="Umumiy Mijoz")

        # Resolve Boiler safely
        boiler_id = (data.get("boiler_id") or "").strip()
        boiler = None
        if boiler_id and boiler_id not in ["undefined", "null"]:
            boiler = Boiler.objects.filter(id=boiler_id).first()

        # Resolve Product safely
        product_id = (data.get("product_id") or "").strip()
        product = None
        if product_id and product_id not in ["undefined", "null"]:
            product = Product.objects.filter(id=product_id).first()

        qty = Decimal(str(data.get("quantity", 1.0) or 1.0))
        unit_price = Decimal(str(data.get("unit_price", 0.0) or 0.0))
        subtotal = qty * unit_price
        disc = Decimal(str(data.get("discount_amount", 0) or 0))
        tax = Decimal(str(data.get("tax_amount", 0) or 0))
        total_amount = subtotal - disc + tax

        sale = Sale.objects.create(
            invoice_number=inv_num,
            customer=customer,
            boiler=boiler,
            product=product,
            quantity=qty,
            unit_price=unit_price,
            subtotal=subtotal,
            discount_amount=disc,
            tax_amount=tax,
            total_amount=total_amount,
            exchange_rate_at_creation=Decimal(str(data.get("exchange_rate_at_creation", 1.0) or 1.0)),
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
