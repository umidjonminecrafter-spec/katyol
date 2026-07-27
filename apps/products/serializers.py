from rest_framework import serializers

class ProductCreateSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    category_id = serializers.CharField()
    material_type_id = serializers.CharField(required=False, allow_null=True)
    unit_id = serializers.CharField()
    supplier_id = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField()  # 'FINISHED_GOOD', 'RAW_MATERIAL', 'SPARE_PART'
    min_stock_level = serializers.FloatField(default=0.0)
    unit_price = serializers.FloatField(default=0.0, min_value=0.0)
    currency = serializers.CharField(default="USD")

class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True)
    category_id = serializers.CharField(required=False, allow_null=True)
    material_type_id = serializers.CharField(required=False, allow_null=True)
    unit_id = serializers.CharField(required=False, allow_null=True)
    supplier_id = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)
    min_stock_level = serializers.FloatField(required=False, allow_null=True)
    unit_price = serializers.FloatField(required=False, allow_null=True)
    currency = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)

class ProductResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    name = serializers.CharField()
    category_id = serializers.CharField()
    category_name = serializers.SerializerMethodField()
    material_type_id = serializers.CharField(allow_null=True, required=False)
    material_type_name = serializers.SerializerMethodField()
    unit_id = serializers.CharField()
    unit_name = serializers.SerializerMethodField()
    supplier_id = serializers.CharField(allow_null=True, required=False)
    supplier_name = serializers.SerializerMethodField()
    type = serializers.CharField()
    unit_price = serializers.FloatField()
    min_stock_level = serializers.FloatField()
    currency = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_category_name(self, obj):
        return obj.category.name if getattr(obj, 'category', None) else None

    def get_material_type_name(self, obj):
        return obj.material_type.name if getattr(obj, 'material_type', None) else None

    def get_unit_name(self, obj):
        return obj.unit.name if getattr(obj, 'unit', None) else None

    def get_supplier_name(self, obj):
        return obj.supplier.name if getattr(obj, 'supplier', None) else None

class RecipeItemSchemaSerializer(serializers.Serializer):
    material_product_id = serializers.CharField()
    quantity = serializers.FloatField()
    waste_percentage = serializers.FloatField(default=0.0)

class RecipeItemResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    recipe_id = serializers.CharField()
    material_product_id = serializers.CharField()
    material_name = serializers.SerializerMethodField()
    quantity = serializers.FloatField()
    waste_percentage = serializers.FloatField()

    def get_material_name(self, obj):
        return obj.material_product.name if getattr(obj, 'material_product', None) else None

class RecipeCreateSerializer(serializers.Serializer):
    recipe_number = serializers.CharField()
    product_id = serializers.CharField()
    version = serializers.CharField(default="v1.0")
    estimated_cost = serializers.FloatField(default=0.0)
    items = RecipeItemSchemaSerializer(many=True, required=False, default=[])

class RecipeResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    recipe_number = serializers.CharField()
    product_id = serializers.CharField()
    version = serializers.CharField()
    estimated_cost = serializers.FloatField()
    status = serializers.CharField()
    items = RecipeItemResponseSerializer(many=True, required=False, default=[])

class BoilerCreateSerializer(serializers.Serializer):
    model_code = serializers.CharField()
    name = serializers.CharField()
    capacity_kw = serializers.FloatField()
    fuel_type = serializers.CharField()
    efficiency_percent = serializers.FloatField(required=False, allow_null=True)
    base_price = serializers.FloatField()
    recipe_id = serializers.CharField(required=False, allow_null=True)
    warranty_type_id = serializers.CharField(required=False, allow_null=True)

class BoilerResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    model_code = serializers.CharField()
    name = serializers.CharField()
    capacity_kw = serializers.FloatField()
    fuel_type = serializers.CharField()
    efficiency_percent = serializers.FloatField(allow_null=True, required=False)
    base_price = serializers.FloatField()
    recipe_id = serializers.CharField(allow_null=True, required=False)
    warranty_type_id = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField()
