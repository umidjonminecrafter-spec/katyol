from rest_framework import serializers

class ProductionBatchCreateSerializer(serializers.Serializer):
    batch_number = serializers.CharField()
    boiler_id = serializers.CharField()
    target_quantity = serializers.IntegerField()
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

class ProductionBatchUpdateSerializer(serializers.Serializer):
    completed_quantity = serializers.IntegerField(required=False, allow_null=True)
    defect_quantity = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)

class ProductionBatchResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    batch_number = serializers.CharField()
    boiler_id = serializers.CharField()
    boiler_name = serializers.SerializerMethodField()
    target_quantity = serializers.IntegerField()
    completed_quantity = serializers.IntegerField()
    defect_quantity = serializers.IntegerField()
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_boiler_name(self, obj):
        return obj.boiler.name if getattr(obj, 'boiler', None) else None
