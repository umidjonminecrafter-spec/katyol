from django.db import models
from core.base_model import BaseModel

class Sale(BaseModel):
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey('master_data.Customer', on_delete=models.CASCADE, db_column='customer_id', related_name='sales')
    boiler = models.ForeignKey('products.Boiler', on_delete=models.SET_NULL, null=True, blank=True, db_column='boiler_id', related_name='sales')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, db_column='product_id', related_name='sales')
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    exchange_rate_at_creation = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)

    payment_status = models.CharField(max_length=20, default="UNPAID")
    delivery_status = models.CharField(max_length=20, default="PENDING")

    class Meta:
        db_table = 'sales'
