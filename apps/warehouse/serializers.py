from rest_framework import serializers

class StockResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    warehouse_id = serializers.CharField()
    warehouse_name = serializers.SerializerMethodField()
    product_id = serializers.CharField()
    product_code = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    quantity = serializers.FloatField()
    reserved_quantity = serializers.FloatField()
    available_quantity = serializers.SerializerMethodField()
    avg_unit_cost = serializers.FloatField()
    updated_at = serializers.DateTimeField()

    def get_warehouse_name(self, obj):
        return obj.warehouse.name if getattr(obj, 'warehouse', None) else ""

    def get_product_code(self, obj):
        return obj.product.code if getattr(obj, 'product', None) else ""

    def get_product_name(self, obj):
        return obj.product.name if getattr(obj, 'product', None) else ""

    def get_available_quantity(self, obj):
        return float(obj.quantity - obj.reserved_quantity)

class StockAdjustmentRequestSerializer(serializers.Serializer):
    warehouse_id = serializers.CharField()
    product_id = serializers.CharField()
    quantity = serializers.FloatField(required=False, allow_null=True)
    quantity_delta = serializers.FloatField(required=False, allow_null=True)
    unit_cost = serializers.FloatField(required=False, allow_null=True, default=0.0)
    movement_type = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="ADJUSTMENT")
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
