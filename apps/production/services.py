from core.exceptions import CustomAppException
from apps.production.models import ProductionBatch

class ProductionService:
    @staticmethod
    def create_batch(data: dict, created_by_id: str) -> ProductionBatch:
        b_num = data.get("batch_number")
        if ProductionBatch.objects.filter(batch_number=b_num).exists():
            raise CustomAppException(message=f"'{b_num}' raqamli ishlab chiqarish partiyasi allaqachon mavjud", error_code="DUPLICATE_BATCH_NUMBER")

        batch = ProductionBatch.objects.create(
            batch_number=b_num,
            boiler_id=data["boiler_id"],
            target_quantity=data["target_quantity"],
            completed_quantity=0,
            defect_quantity=0,
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            status="PLANNED",
            created_by_id=created_by_id
        )
        return batch

    @staticmethod
    def update_batch(batch_id: str, data: dict, updated_by_id: str) -> ProductionBatch:
        try:
            batch = ProductionBatch.objects.get(id=batch_id)
        except ProductionBatch.DoesNotExist:
            raise CustomAppException(message="Ishlab chiqarish partiyasi topilmadi", status_code=404)

        for field, value in data.items():
            if value is not None and hasattr(batch, field):
                setattr(batch, field, value)

        batch.updated_by_id = updated_by_id
        batch.save()
        return batch

    @staticmethod
    def get_multi(
        page: int = 1,
        limit: int = 20,
        status: str = None
    ):
        qs = ProductionBatch.objects.all()

        if status:
            qs = qs.filter(status=status)

        total = qs.count()

        skip = (page - 1) * limit
        items = list(qs.order_by('-created_at')[skip:skip + limit])

        return items, total
