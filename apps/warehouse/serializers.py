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
        return obj.warehouse.name if getattr(obj, 'warehouse', None) else None

    def get_product_code(self, obj):
        return obj.product.code if getattr(obj, 'product', None) else None

    def get_product_name(self, obj):
        return obj.product.name if getattr(obj, 'product', None) else None

    def get_available_quantity(self, obj):
        return float(obj.quantity - obj.reserved_quantity)

class StockAdjustmentRequestSerializer(serializers.Serializer):
    warehouse_id = serializers.CharField()
    product_id = serializers.CharField()
    quantity_delta = serializers.FloatField()
    notes = serializers.CharField(required=False, allow_null=True)
