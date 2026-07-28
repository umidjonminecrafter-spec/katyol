from core.exceptions import CustomAppException
from core.safe_delete import SafeDeleteService
from apps.master_data.models import (
    ProductCategory, MaterialType, Unit, Supplier, Customer,
    Warehouse, WarrantyType, CustomerType, ServiceType, Priority, OrderStatus, ExpenseType, SalaryType
)

MASTER_DATA_MODELS = {
    "product-categories": ProductCategory,
    "material-types": MaterialType,
    "units": Unit,
    "suppliers": Supplier,
    "customers": Customer,
    "warehouses": Warehouse,
    "warranty-types": WarrantyType,
    "customer-types": CustomerType,
    "service-types": ServiceType,
    "priorities": Priority,
    "order-statuses": OrderStatus,
    "expense-types": ExpenseType,
    "salary-types": SalaryType,
}

class MasterDataService:
    @staticmethod
    def get_model(entity_key: str):
        model = MASTER_DATA_MODELS.get(entity_key)
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
        if "code" in data and data["code"]:
            if model.objects.filter(code=data["code"]).exists():
                raise CustomAppException(message=f"'{data['code']}' kodli master data allaqachon mavjud", error_code="DUPLICATE_CODE")
        
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
