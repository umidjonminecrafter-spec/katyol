from django.contrib import admin
from apps.master_data.models import (
    ProductCategory, MaterialType, Unit, Supplier, Customer, Warehouse,
    WarrantyType, CustomerType, ServiceType, Priority, OrderStatus, ExpenseType, Company
)

admin.site.register(ProductCategory)
admin.site.register(MaterialType)
admin.site.register(Unit)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Warehouse)
admin.site.register(WarrantyType)
admin.site.register(CustomerType)
admin.site.register(ServiceType)
admin.site.register(Priority)
admin.site.register(OrderStatus)
admin.site.register(ExpenseType)
admin.site.register(Company)
