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
    position_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    department = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    salary_amount = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    salary_type_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    hire_date = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')


class UserInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    full_name = serializers.CharField()
    role = serializers.CharField()
    username = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    organization_id = serializers.SerializerMethodField()
    branch_id = serializers.SerializerMethodField()
    salary_amount = serializers.SerializerMethodField()
    salary_type_id = serializers.SerializerMethodField()
    hire_date = serializers.SerializerMethodField()

    def get_username(self, obj):
        return getattr(obj, 'username', '') or ''

    def get_phone(self, obj):
        return getattr(obj, 'phone', '') or ''

    def get_department(self, obj):
        return getattr(obj, 'department', '') or ''

    def get_organization_name(self, obj):
        return getattr(obj, 'organization_name', '') or ''

    def get_branch_name(self, obj):
        return getattr(obj, 'branch_name', '') or ''

    def get_organization_id(self, obj):
        val = getattr(obj, 'organization_id', None)
        if not val and hasattr(obj, 'organization') and obj.organization:
            val = obj.organization.id
        return val or ''

    def get_branch_id(self, obj):
        val = getattr(obj, 'branch_id', None)
        if not val and hasattr(obj, 'branch') and obj.branch:
            val = obj.branch.id
        return val or ''

    def get_salary_amount(self, obj):
        return getattr(obj, 'salary_amount', '') or ''

    def get_salary_type_id(self, obj):
        return getattr(obj, 'salary_type_id', '') or ''

    def get_hire_date(self, obj):
        return getattr(obj, 'hire_date', '') or ''


class RefreshRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class BranchCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')


class BranchResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    organization_id = serializers.SerializerMethodField()
    name = serializers.CharField()
    code = serializers.CharField()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    status = serializers.CharField()

    def get_organization_id(self, obj):
        return getattr(obj, 'organization_id', '') or ''

    def get_address(self, obj):
        return getattr(obj, 'address', '') or ''

    def get_phone(self, obj):
        return getattr(obj, 'phone', '') or ''


class PositionCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')
    permissions = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='')


class PositionResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    status = serializers.CharField()

    def get_description(self, obj):
        return getattr(obj, 'description', '') or ''

    def get_permissions(self, obj):
        return getattr(obj, 'permissions', '') or ''
