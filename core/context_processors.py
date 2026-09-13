from .permissions import (
    is_admin,
    is_vkh_engineer,
    is_pto_engineer,
    is_management,
)


def user_permissions(request):
    user = request.user

    return {
        "user_is_admin": is_admin(user),
        "user_is_vkh": is_vkh_engineer(user),
        "user_is_pto": is_pto_engineer(user),
        "user_is_management": is_management(user),
    }