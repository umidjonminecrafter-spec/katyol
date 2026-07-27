from rest_framework import serializers

class TransactionCreateSerializer(serializers.Serializer):
    transaction_number = serializers.CharField()
    type = serializers.CharField()
    expense_type_id = serializers.CharField(required=False, allow_null=True)
    amount = serializers.FloatField()
    currency = serializers.CharField(default="USD")
    reference_id = serializers.CharField(required=False, allow_null=True)
    transaction_date = serializers.DateField()
    notes = serializers.CharField(required=False, allow_null=True)

class TransactionResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    transaction_number = serializers.CharField()
    type = serializers.CharField()
    expense_type_id = serializers.CharField(allow_null=True, required=False)
    amount = serializers.FloatField()
    currency = serializers.CharField()
    reference_id = serializers.CharField(allow_null=True, required=False)
    transaction_date = serializers.DateField()
    notes = serializers.CharField(allow_null=True, required=False)
    created_at = serializers.DateTimeField()
