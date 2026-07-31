from rest_framework import serializers

class OrderCreateSerializer(serializers.Serializer):
    order_number = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    order_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    orderName = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    customer_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    customer_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    customerName = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    boiler_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    boiler_model_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    boilerModelName = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    quantity = serializers.FloatField(required=False, allow_null=True, default=1.0)
    unit_price = serializers.FloatField(required=False, allow_null=True, default=0.0)
    unitPrice = serializers.FloatField(required=False, allow_null=True, default=0.0)
    total_amount = serializers.FloatField(required=False, allow_null=True, default=0.0)
    totalAmount = serializers.FloatField(required=False, allow_null=True, default=0.0)
    priority = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="HIGH")
    status = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="NEW")
    delivery_date = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    deliveryDate = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")

class OrderResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    order_number = serializers.CharField()
    orderNumber = serializers.SerializerMethodField()
    order_name = serializers.SerializerMethodField()
    orderName = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()
    customerId = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    customerName = serializers.SerializerMethodField()
    boiler_id = serializers.SerializerMethodField()
    boilerId = serializers.SerializerMethodField()
    boiler_model_name = serializers.SerializerMethodField()
    boilerModelName = serializers.SerializerMethodField()
    quantity = serializers.FloatField()
    unit_price = serializers.FloatField()
    unitPrice = serializers.SerializerMethodField()
    total_amount = serializers.FloatField()
    totalAmount = serializers.SerializerMethodField()
    priority = serializers.CharField()
    status = serializers.CharField()
    delivery_date = serializers.SerializerMethodField()
    deliveryDate = serializers.SerializerMethodField()
    notes = serializers.CharField(allow_null=True, required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_orderNumber(self, obj):
        return obj.order_number

    def get_order_name(self, obj):
        return obj.order_name or ""

    def get_orderName(self, obj):
        return obj.order_name or ""

    def get_customer_id(self, obj):
        return obj.customer.id if getattr(obj, 'customer', None) else ""

    def get_customerId(self, obj):
        return obj.customer.id if getattr(obj, 'customer', None) else ""

    def get_customer_name(self, obj):
        if getattr(obj, 'customer', None):
            return obj.customer.name
        return obj.customer_name or ""

    def get_customerName(self, obj):
        return self.get_customer_name(obj)

    def get_boiler_id(self, obj):
        return obj.boiler.id if getattr(obj, 'boiler', None) else ""

    def get_boilerId(self, obj):
        return obj.boiler.id if getattr(obj, 'boiler', None) else ""

    def get_boiler_model_name(self, obj):
        if getattr(obj, 'boiler', None):
            return obj.boiler.name
        return obj.boiler_model_name or ""

    def get_boilerModelName(self, obj):
        return self.get_boiler_model_name(obj)

    def get_unitPrice(self, obj):
        return float(obj.unit_price or 0.0)

    def get_totalAmount(self, obj):
        return float(obj.total_amount or 0.0)

    def get_delivery_date(self, obj):
        return obj.delivery_date.isoformat() if getattr(obj, 'delivery_date', None) else ""

    def get_deliveryDate(self, obj):
        return self.get_delivery_date(obj)
