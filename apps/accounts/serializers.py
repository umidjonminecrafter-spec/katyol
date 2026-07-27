from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    full_name = serializers.CharField()
    organization_name = serializers.CharField()
    branch_name = serializers.CharField()
    currency = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    full_name = serializers.CharField()
    role = serializers.CharField(default='EMPLOYEE')
    position_id = serializers.CharField(required=False, allow_null=True, default=None)
    department = serializers.CharField(required=False, allow_null=True, default=None)
    salary_amount = serializers.CharField(required=False, allow_null=True, default=None)
    salary_type_id = serializers.CharField(required=False, allow_null=True, default=None)
    hire_date = serializers.CharField(required=False, allow_null=True, default=None)


class UserInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    full_name = serializers.CharField()
    role = serializers.CharField()
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, allow_null=True)
    department = serializers.CharField(required=False, allow_null=True)
    organization_name = serializers.CharField(required=False, allow_null=True)
    branch_name = serializers.CharField(required=False, allow_null=True)
    organization_id = serializers.SerializerMethodField()
    branch_id = serializers.SerializerMethodField()
    salary_amount = serializers.CharField(required=False, allow_null=True)
    salary_type_id = serializers.CharField(required=False, allow_null=True)
    hire_date = serializers.CharField(required=False, allow_null=True)

    def get_organization_id(self, obj):
        return getattr(obj, 'organization_id', None) or (obj.organization_id if hasattr(obj, 'organization_id') else None)

    def get_branch_id(self, obj):
        return getattr(obj, 'branch_id', None) or (obj.branch_id if hasattr(obj, 'branch_id') else None)


class RefreshRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class BranchCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    address = serializers.CharField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)


class BranchResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    organization_id = serializers.SerializerMethodField()
    name = serializers.CharField()
    code = serializers.CharField()
    address = serializers.CharField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    status = serializers.CharField()

    def get_organization_id(self, obj):
        return obj.organization_id if hasattr(obj, 'organization_id') else None


class PositionCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True, default=None)
    permissions = serializers.CharField(required=False, allow_null=True, default=None)


class PositionResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    permissions = serializers.CharField(allow_null=True)
    status = serializers.CharField()
