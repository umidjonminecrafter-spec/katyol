from core.exceptions import CustomAppException
from core.safe_delete import SafeDeleteService
from apps.master_data.models import (
    ProductCategory, SupplierCategory, MaterialType, Unit, Supplier, Customer,
    Warehouse, WarrantyType, CustomerType, ServiceType, Priority, OrderStatus, ExpenseType, SalaryType
)

MASTER_DATA_MODELS = {
    "product-categories": ProductCategory,
    "product-category": ProductCategory,
    "supplier-categories": SupplierCategory,
    "supplier-category": SupplierCategory,
    "material-types": MaterialType,
    "material-type": MaterialType,
    "units": Unit,
    "unit": Unit,
    "suppliers": Supplier,
    "supplier": Supplier,
    "customers": Customer,
    "customer": Customer,
    "warehouses": Warehouse,
    "warehouse": Warehouse,
    "warranty-types": WarrantyType,
    "warranty-type": WarrantyType,
    "customer-types": CustomerType,
    "customer-type": CustomerType,
    "service-types": ServiceType,
    "service-type": ServiceType,
    "priorities": Priority,
    "priority": Priority,
    "order-statuses": OrderStatus,
    "order-status": OrderStatus,
    "expense-types": ExpenseType,
    "expense-type": ExpenseType,
    "salary-types": SalaryType,
    "salary-type": SalaryType,
}

class MasterDataService:
    @staticmethod
    def get_model(entity_key: str):
        normalized_key = str(entity_key).lower().strip().replace('_', '-')
        model = MASTER_DATA_MODELS.get(normalized_key)
        if not model:
            raise CustomAppException(message=f"Entity key '{entity_key}' topilmadi", status_code=404)
        return model

    @classmethod
    def get_multi(cls, entity_key: str, include_archived: bool = False):
        model = cls.get_model(entity_key)
        qs = model.objects.all()
        if not include_archived:
            qs = qs.exclude(status="ARCHIVED")
        items = list(qs.order_by("-created_at")[:1000])
        total = qs.count()
        return items, total

    @classmethod
    def create(cls, entity_key: str, data: dict, created_by_id: str):
        model = cls.get_model(entity_key)
        code_val = data.get("code")
        if code_val and str(code_val).strip():
            code_val = str(code_val).strip()
            if model.objects.filter(code=code_val).exists():
                raise CustomAppException(message=f"'{code_val}' kodli master data allaqachon mavjud", error_code="DUPLICATE_CODE")
            data["code"] = code_val
        else:
            import uuid
            name_prefix = data.get("name", "ITEM").strip().upper().replace(" ", "_")[:15]
            data["code"] = f"{name_prefix}_{str(uuid.uuid4())[:6]}"
        
        model_fields = {f.name for f in model._meta.get_fields()}
        valid_data = {k: v for k, v in data.items() if k in model_fields and v is not None}

        if created_by_id and "created_by_id" in model_fields:
            valid_data["created_by_id"] = created_by_id

        item = model.objects.create(**valid_data)
        return item


    @classmethod
    def update(cls, entity_key: str, item_id: str, data: dict, updated_by_id: str):
        model = cls.get_model(entity_key)
        try:
            item = model.objects.get(id=item_id)
        except model.DoesNotExist:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        
        model_fields = {f.name for f in model._meta.get_fields()}
        for k, v in data.items():
            if k in model_fields and v is not None and hasattr(item, k):
                setattr(item, k, v)
        if updated_by_id and "updated_by_id" in model_fields:
            item.updated_by_id = updated_by_id
        item.save()
        return item


    @classmethod
    def archive(cls, entity_key: str, item_id: str, updated_by_id: str):
        model = cls.get_model(entity_key)
        try:
            item = model.objects.get(id=item_id)
        except model.DoesNotExist:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        item.status = "ARCHIVED"
        item.is_active = False
        if updated_by_id and hasattr(item, "updated_by_id"):
            item.updated_by_id = updated_by_id
        item.save()
        return item

    @classmethod
    def restore(cls, entity_key: str, item_id: str, updated_by_id: str):
        model = cls.get_model(entity_key)
        try:
            item = model.objects.get(id=item_id)
        except model.DoesNotExist:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)
        item.status = "ACTIVE"
        item.is_active = True
        if updated_by_id and hasattr(item, "updated_by_id"):
            item.updated_by_id = updated_by_id
        item.save()
        return item

    @classmethod
    def delete(cls, entity_key: str, item_id: str):
        model = cls.get_model(entity_key)
        try:
            item = model.objects.get(id=item_id)
        except model.DoesNotExist:
            raise CustomAppException(message="Master data ob'ekti topilmadi", status_code=404)

        SafeDeleteService.check_entity_references(entity_key, item_id)
        item.delete()
        return True
