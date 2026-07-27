from django.db.models import Q
from core.exceptions import CustomAppException
from core.safe_delete import SafeDeleteService
from apps.products.models import Product

class ProductService:
    @staticmethod
    def get_multi(
        page: int = 1,
        limit: int = 20,
        search: str = None,
        category_id: str = None,
        product_type: str = None,
        status: str = "ACTIVE"
    ):
        qs = Product.objects.all()

        if status:
            qs = qs.filter(status=status)

        if category_id:
            qs = qs.filter(category_id=category_id)

        if product_type:
            qs = qs.filter(type=product_type)

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(code__icontains=search))

        total = qs.count()

        skip = (page - 1) * limit
        items = list(qs.order_by('-created_at')[skip:skip + limit])

        return items, total

    @staticmethod
    def create(data: dict, created_by_id: str) -> Product:
        code = data.get("code")
        if Product.objects.filter(code=code).exists():
            raise CustomAppException(
                message="Ushbu mahsulot kodi tizimda allaqachon mavjud",
                error_code="VALIDATION_ERROR",
                errors=[{"field": "code", "message": "Ushbu mahsulot kodi tizimda allaqachon mavjud"}]
            )
        
        if created_by_id and hasattr(Product, "created_by_id"):
            data["created_by_id"] = created_by_id

        product = Product.objects.create(**data)
        return product

    @staticmethod
    def get_by_id(product_id: str) -> Product:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise CustomAppException(message="Mahsulot topilmadi", status_code=404)

    @staticmethod
    def update(product_id: str, data: dict, updated_by_id: str) -> Product:
        item = ProductService.get_by_id(product_id)
        for k, v in data.items():
            if hasattr(item, k) and v is not None:
                setattr(item, k, v)
        if updated_by_id:
            item.updated_by_id = updated_by_id
        item.save()
        return item

    @staticmethod
    def delete(product_id: str) -> bool:
        item = ProductService.get_by_id(product_id)
        SafeDeleteService.check_entity_references("products", product_id)
        item.delete()
        return True
