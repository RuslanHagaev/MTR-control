from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    Object,
    Position,
    ProjectCode,
    Supplier,
    Material,
    MaterialDocument,
    MaterialAct,
    NormativeDocument,
    AuditLog,
)

from .middleware import get_current_user


TRACKED_MODELS = (
    Object,
    Position,
    ProjectCode,
    Supplier,
    Material,
    MaterialDocument,
    MaterialAct,
    NormativeDocument,
)


def get_object_name(instance):

    if hasattr(instance, "name") and instance.name:
        return str(instance.name)

    if hasattr(instance, "designation") and instance.designation:
        return str(instance.designation)

    if hasattr(instance, "number") and instance.number:
        return f"АоРПИ № {instance.number}"

    return str(instance)


@receiver(post_save)
def log_model_save(
    sender,
    instance,
    created,
    **kwargs,
):

    if sender not in TRACKED_MODELS:
        return

    user = get_current_user()

    AuditLog.objects.create(
        user=user,
        action=(
            AuditLog.Action.CREATE
            if created
            else AuditLog.Action.UPDATE
        ),
        object_type=sender.__name__,
        object_id=instance.pk,
        object_name=get_object_name(instance),
        description=(
            "Создан объект"
            if created
            else "Изменён объект"
        ),
    )


@receiver(post_delete)
def log_model_delete(
    sender,
    instance,
    **kwargs,
):

    if sender not in TRACKED_MODELS:
        return

    user = get_current_user()

    AuditLog.objects.create(
        user=user,
        action=AuditLog.Action.DELETE,
        object_type=sender.__name__,
        object_id=instance.pk,
        object_name=get_object_name(instance),
        description="Удалён объект",
    )