from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .models import (
    Object,
    Position,
    ProjectCode,
    Material,
    MaterialDocument,
    MaterialAct,
)


# ============================================================
# ПРОВЕРКА АВТОРИЗАЦИИ
# ============================================================

def is_authenticated(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
    )


# ============================================================
# ПОЛУЧЕНИЕ РОЛИ
# ============================================================

def get_role(user):

    if not is_authenticated(user):
        return None

    return user.profile.role


# ============================================================
# АДМИНИСТРАТОР
# ============================================================

def is_admin(user):

    return (
        is_authenticated(user)
        and user.profile.role
        == user.profile.Role.ADMIN
    )


# ============================================================
# ВХК
# ============================================================

def is_vkh_engineer(user):

    if not is_authenticated(user):
        return False

    return user.profile.role in (
        user.profile.Role.VKH_ENGINEER,
        user.profile.Role.LEAD_VKH_ENGINEER,
    )


# ============================================================
# ПТО
# ============================================================

def is_pto_engineer(user):

    return (
        is_authenticated(user)
        and user.profile.role
        == user.profile.Role.PTO_ENGINEER
    )


# ============================================================
# РУКОВОДСТВО
# ============================================================

def is_management(user):

    return (
        is_authenticated(user)
        and user.profile.role
        == user.profile.Role.MANAGEMENT
    )


# ============================================================
# ГОСТЬ
# ============================================================

def is_guest(user):

    return (
        is_authenticated(user)
        and user.profile.role
        == user.profile.Role.GUEST
    )


# ============================================================
# МОЖЕТ ЛИ ПОЛЬЗОВАТЕЛЬ ВИДЕТЬ ОБЪЕКТ
# ============================================================

def can_view_object(user, obj):

    if not is_authenticated(user):
        return False

    if is_admin(user):
        return True

    if is_guest(user):
        return False

    return user.profile.allowed_objects.filter(
        id=obj.id
    ).exists()


# ============================================================
# МОЖЕТ ЛИ ПОЛЬЗОВАТЕЛЬ РЕДАКТИРОВАТЬ
# ============================================================

def can_edit_object(user, obj):

    if not can_view_object(user, obj):
        return False

    if is_admin(user):
        return True

    if is_vkh_engineer(user):
        return True

    return False


# ============================================================
# МОЖЕТ ЛИ ПОЛЬЗОВАТЕЛЬ ТОЛЬКО ПРОСМАТРИВАТЬ
# ============================================================

def is_read_only(user):

    if not is_authenticated(user):
        return True

    return (
        is_pto_engineer(user)
        or is_management(user)
    )


# ============================================================
# ПОЛУЧЕНИЕ ОБЪЕКТА И ПРОВЕРКА ДОСТУПА
# ============================================================

def get_allowed_object(user, object_id):

    obj = get_object_or_404(
        Object,
        id=object_id
    )

    if not can_view_object(user, obj):
        raise PermissionError

    return obj


# ============================================================
# ПРОВЕРКА ОБЪЕКТА ДЛЯ ЛЮБОГО СВЯЗАННОГО ОБЪЕКТА
# ============================================================

def can_view_position(user, position):

    return can_view_object(
        user,
        position.object
    )


def can_view_project_code(user, project_code):

    return can_view_object(
        user,
        project_code.position.object
    )


def can_view_material(user, material):

    return can_view_object(
        user,
        material.project_code.position.object
    )


def can_view_document(user, document):

    return can_view_material(
        user,
        document.material
    )
def can_edit_document(user, document):
    return can_edit_material(
        user,
        document.material
    )

def can_view_act(user, act):

    return can_view_material(
        user,
        act.material
    )

def can_edit_act(user, act):
    return can_edit_material(
        user,
        act.material
    )
# ============================================================
# ДЕКОРАТОР: ТРЕБУЕТ АВТОРИЗАЦИИ
# ============================================================

def login_required_custom(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return HttpResponseForbidden(
                "Необходимо войти в систему."
            )

        if not hasattr(request.user, "profile"):

            return HttpResponseForbidden(
                "Профиль пользователя не настроен."
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# ДЕКОРАТОР: ТРЕБУЕТ АДМИНИСТРАТОРА
# ============================================================

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not is_admin(request.user):

            return HttpResponseForbidden(
                "Доступ разрешён только администратору."
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# ДЕКОРАТОР: ТРЕБУЕТ ВХК
# ============================================================

def vkh_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not is_vkh_engineer(request.user):

            return HttpResponseForbidden(
                "Доступ разрешён только инженерам ВХК."
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper

# ============================================================
# ПРАВА НА ПОЗИЦИЮ
# ============================================================

def can_edit_position(user, position):
    return can_edit_object(
        user,
        position.object
    )


# ============================================================
# ПРАВА НА ШИФР ПРОЕКТА
# ============================================================

def can_edit_project_code(user, project_code):
    return can_edit_object(
        user,
        project_code.position.object
    )


# ============================================================
# ПРАВА НА МАТЕРИАЛ
# ============================================================

def can_edit_material(user, material):
    return can_edit_object(
        user,
        material.project_code.position.object
    )


# ============================================================
# ПРАВА НА ДОКУМЕНТ
# ============================================================

def can_edit_document(user, document):
    return can_edit_material(
        user,
        document.material
    )


# ============================================================
# ПРАВА НА АоРПИ
# ============================================================

def can_edit_act(user, act):
    return can_edit_material(
        user,
        act.material
    )