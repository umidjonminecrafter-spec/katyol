from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from core.audit_helper import record_audit_log
from core.exceptions import CustomAppException
from apps.accounts.models import User, Organization, Branch
from rest_framework import status


class AuthService:
    @staticmethod
    def register_user(data, request=None):
        if User.objects.filter(username=data['phone']).exists():
            raise CustomAppException(
                message='Ushbu telefon raqami bilan foydalanuvchi allaqachon mavjud',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Create Organization
        org = Organization.objects.create(name=data['organization_name'])

        # 2. Create default Branch
        branch = Branch.objects.create(
            organization=org,
            name=data['branch_name'],
            code='MAIN-BRANCH',
        )

        # 3. Create Admin User linked to organization & branch
        user = User.objects.create(
            username=data['phone'],
            hashed_password=get_password_hash(data['password']),
            full_name=data['full_name'],
            phone=data['phone'],
            role='ADMIN',
            organization_name=data['organization_name'],
            branch_name=data['branch_name'],
            organization=org,
            branch=branch,
            status='ACTIVE',
        )

        from apps.master_data.models import Company
        company = Company.objects.first()
        if not company:
            Company.objects.create(
                name=data['organization_name'],
                phone=data['phone'],
                currency=data.get('currency', 'USD'),
                timezone='Asia/Tashkent (UTC+5)',
                date_format='YYYY-MM-DD',
            )
        else:
            company.name = data['organization_name']
            company.phone = data['phone']
            company.currency = data.get('currency', 'USD')
            company.save()

        return user

    @staticmethod
    def create_employee_user(data, creator):
        if User.objects.filter(username=data['phone']).exists():
            raise CustomAppException(
                message='Ushbu telefon raqami bilan foydalanuvchi allaqachon mavjud',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(
            username=data['phone'],
            hashed_password=get_password_hash(data['password']),
            full_name=data['full_name'],
            phone=data['phone'],
            role=data.get('role', 'EMPLOYEE'),
            position_id=data.get('position_id'),
            department=data.get('department'),
            salary_amount=data.get('salary_amount', ''),
            salary_type_id=data.get('salary_type_id', ''),
            hire_date=data.get('hire_date', ''),
            organization_name=creator.organization_name,
            branch_name=creator.branch_name,
            organization=creator.organization,
            branch=creator.branch,
            status='ACTIVE',
        )
        return user


    @staticmethod
    def list_employees(creator):
        return list(User.objects.filter(
            organization_name=creator.organization_name,
            branch_name=creator.branch_name,
        ))

    @staticmethod
    def authenticate_user(data, request=None):
        try:
            user = User.objects.get(username=data['username'], status='ACTIVE')
        except User.DoesNotExist:
            raise CustomAppException(
                message='USER_NOT_FOUND',
                error_code='NOT_FOUND',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not verify_password(data['password'], user.hashed_password):
            raise CustomAppException(
                message="Noto'g'ri parol",
                error_code='UNAUTHORIZED',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id)

        record_audit_log(
            action='LOGIN',
            entity_name='USER',
            entity_id=user.id,
            actor_id=user.id,
            request=request,
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': user,
        }

    @staticmethod
    def refresh_access_token(refresh_token_str):
        payload = decode_token(refresh_token_str)
        if not payload or payload.get('type') != 'refresh':
            raise CustomAppException(
                message='Yaroqsiz refresh token',
                error_code='UNAUTHORIZED',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        user_id = payload.get('sub')
        try:
            user = User.objects.get(id=user_id, status='ACTIVE')
        except User.DoesNotExist:
            raise CustomAppException(
                message='Foydalanuvchi topilmadi',
                error_code='UNAUTHORIZED',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return create_access_token(subject=user.id, role=user.role)
