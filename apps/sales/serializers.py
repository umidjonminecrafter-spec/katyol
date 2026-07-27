from rest_framework import serializers

class SaleCreateSerializer(serializers.Serializer):
    invoice_number = serializers.CharField()
    customer_id = serializers.CharField()
    boiler_id = serializers.CharField(required=False, allow_null=True)
    product_id = serializers.CharField(required=False, allow_null=True)
    quantity = serializers.FloatField()
    unit_price = serializers.FloatField()
    discount_amount = serializers.FloatField(default=0.0)
    tax_amount = serializers.FloatField(default=0.0)
    exchange_rate_at_creation = serializers.FloatField(default=1.0)

class SaleUpdateStatusSerializer(serializers.Serializer):
    payment_status = serializers.CharField(required=False, allow_null=True)
    delivery_status = serializers.CharField(required=False, allow_null=True)

class SaleResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    invoice_number = serializers.CharField()
    customer_id = serializers.CharField()
    customer_name = serializers.SerializerMethodField()
    boiler_id = serializers.CharField(allow_null=True, required=False)
    product_id = serializers.CharField(allow_null=True, required=False)
    quantity = serializers.FloatField()
    unit_price = serializers.FloatField()
    subtotal = serializers.FloatField()
    discount_amount = serializers.FloatField()
    tax_amount = serializers.FloatField()
    total_amount = serializers.FloatField()
    exchange_rate_at_creation = serializers.FloatField()
    payment_status = serializers.CharField()
    delivery_status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_customer_name(self, obj):
        return obj.customer.name if getattr(obj, 'customer', None) else None
