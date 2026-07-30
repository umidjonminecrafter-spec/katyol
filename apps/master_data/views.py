from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticated, require_roles
from core.audit_helper import record_audit_log
from core.exceptions import CustomAppException
from apps.master_data.models import Company
from apps.master_data.services import MasterDataService
from apps.master_data.serializers import (
    MasterDataCreateSerializer, MasterDataUpdateSerializer, MasterDataResponseSerializer,
    CompanyUpdateSerializer, CompanyResponseSerializer
)

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def master_data_list_create_view(request, entity_key):
    if request.method == 'GET':
        include_archived = request.query_params.get('include_archived', 'false').lower() == 'true'
        items, total = MasterDataService.get_multi(entity_key, include_archived=include_archived)
        resp = MasterDataResponseSerializer(items, many=True).data
        return Response({"success": True, "data": resp})

    # POST (create)
    serializer = MasterDataCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    body_data = serializer.validated_data
    item = MasterDataService.create(entity_key, body_data, created_by_id=request.user.id)
    record_audit_log(
        action="CREATE",
        entity_name=entity_key.upper(),
        entity_id=item.id,
        actor_id=request.user.id,
        new_values=body_data,
        request=request
    )
    return Response({"success": True, "data": MasterDataResponseSerializer(item).data}, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def master_data_detail_view(request, entity_key, id):
    model = MasterDataService.get_model(entity_key)
    try:
        item = model.objects.get(id=id)
    except model.DoesNotExist:
        raise CustomAppException(message="Master data topilmadi", status_code=404)

    if request.method == 'GET':
        return Response({"success": True, "data": MasterDataResponseSerializer(item).data})

    if request.method == 'PUT':
        serializer = MasterDataUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        body_data = {k: v for k, v in serializer.validated_data.items() if v is not None}
        updated_item = MasterDataService.update(entity_key, id, body_data, updated_by_id=request.user.id)
        record_audit_log(
            action="UPDATE",
            entity_name=entity_key.upper(),
            entity_id=id,
            actor_id=request.user.id,
            new_values=body_data,
            request=request
        )
        return Response({"success": True, "data": MasterDataResponseSerializer(updated_item).data})

    # DELETE
    MasterDataService.delete(entity_key, id)
    record_audit_log(
        action="DELETE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=request.user.id,
        request=request
    )
    return Response({"success": True, "data": {"id": id, "deleted": True}})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def archive_master_data_view(request, entity_key, id):
    item = MasterDataService.archive(entity_key, id, updated_by_id=request.user.id)
    record_audit_log(
        action="ARCHIVE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=request.user.id,
        request=request
    )
    return Response({"success": True, "data": MasterDataResponseSerializer(item).data})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def restore_master_data_view(request, entity_key, id):
    item = MasterDataService.restore(entity_key, id, updated_by_id=request.user.id)
    record_audit_log(
        action="RESTORE",
        entity_name=entity_key.upper(),
        entity_id=id,
        actor_id=request.user.id,
        request=request
    )
    return Response({"success": True, "data": MasterDataResponseSerializer(item).data})

@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def company_profile_view(request):
    company = Company.objects.first()
    if not company:
        company = Company.objects.create(
            name="Kotyol Manufacturing",
            phone="+998 (90) 123-45-67",
            website="https://kotyol.uz",
            address="Toshkent sh., Chilonzor tumani, 5-daha",
            description="Yuqori sifatli isitish kotyollari ishlab chiqarish zavodi.",
            currency="USD",
            timezone="Asia/Tashkent (UTC+5)",
            date_format="YYYY-MM-DD"
        )

    if request.method == 'GET':
        return Response({"success": True, "data": CompanyResponseSerializer(company).data})

    # PUT
    serializer = CompanyUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    update_data = {k: v for k, v in serializer.validated_data.items() if v is not None}
    for key, value in update_data.items():
        setattr(company, key, value)
    company.save()

    record_audit_log(
        action="UPDATE",
        entity_name="COMPANY_PROFILE",
        entity_id=company.id,
        actor_id=request.user.id,
        new_values=update_data,
        request=request
    )
    return Response({"success": True, "data": CompanyResponseSerializer(company).data})
