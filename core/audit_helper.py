import uuid


def record_audit_log(action, entity_name, entity_id, actor_id=None,
                     old_values=None, new_values=None, request=None):
    from apps.audit.models import AuditLog

    ip_address = None
    user_agent = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

    AuditLog.objects.create(
        id=str(uuid.uuid4()),
        actor_id=actor_id,
        action=action,
        entity_name=entity_name,
        entity_id=str(entity_id),
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent,
    )
