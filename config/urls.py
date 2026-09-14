from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views


urlpatterns = [

    # ==================================================
    # ГЛАВНАЯ
    # ==================================================

    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "search/",
        views.search,
        name="search",
    ),

        # ==================================================
    # НОРМАТИВНЫЕ ДОКУМЕНТЫ
    # ==================================================
    path(
        "normative-documents/",
        views.normative_documents,
        name="normative_documents",
    ),
    path(
        "normative-document/<int:document_id>/",
        views.normative_document_detail,
        name="normative_document_detail",
    ),
    # ==================================================
    # ИСТОРИЯ ИЗМЕНЕНИЙ
    # ==================================================
    path(
        "audit-log/",
        views.audit_log,
        name="audit_log",
    ),
    # ==================================================
    # АВТОРИЗАЦИЯ
    # ==================================================
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="core/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "profile/",
        views.profile,
        name="profile",
    ),
    # ==================================================
    # АДМИНКА
    # ==================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==================================================
    # СПИСОК МТР ПО СТАТУСУ
    # ==================================================

    path(
        "materials/status/<str:status>/",
        views.material_status_list,
        name="material_status_list",
    ),

    # ==================================================
    # ОБЪЕКТ
    # ==================================================

    path(
        "object/<int:object_id>/",
        views.object_detail,
        name="object_detail",
    ),

    # ==================================================
    # ПОЗИЦИЯ
    # ==================================================

    path(
        "position/<int:position_id>/",
        views.position_detail,
        name="position_detail",
    ),

    path(
        "object/<int:object_id>/position/add/",
        views.position_create,
        name="position_create",
    ),

    # ==================================================
    # ШИФР
    # ==================================================

    path(
        "project-code/<int:project_code_id>/",
        views.project_code_detail,
        name="project_code_detail",
    ),

    path(
        "position/<int:position_id>/project-code/add/",
        views.project_code_create,
        name="project_code_create",
    ),

    # ==================================================
    # МАТЕРИАЛ
    # ==================================================

    path(
        "project-code/<int:project_code_id>/material/add/",
        views.material_create,
        name="material_create",
    ),

    path(
        "material/<int:material_id>/",
        views.material_detail,
        name="material_detail",
    ),

    path(
        "material/<int:material_id>/edit/",
        views.material_edit,
        name="material_edit",
    ),

    path(
        "material/<int:material_id>/delete/",
        views.material_delete,
        name="material_delete",
    ),

    # ==================================================
    # ДОКУМЕНТЫ МАТЕРИАЛА
    # ==================================================

    path(
        "material/<int:material_id>/documents/",
        views.material_documents,
        name="material_documents",
    ),

    path(
        "material-document/<int:document_id>/delete/",
        views.material_document_delete,
        name="material_document_delete",
    ),

    # ==================================================
    # АоРПИ
    # ==================================================

    path(
        "material/<int:material_id>/act/add/",
        views.material_act_create,
        name="material_act_create",
    ),

    path(
        "act/<int:act_id>/",
        views.material_act_detail,
        name="material_act_detail",
    ),

    path(
        "act/<int:act_id>/edit/",
        views.material_act_edit,
        name="material_act_edit",
    ),

    path(
        "act/<int:act_id>/generate/",
        views.material_act_generate,
        name="material_act_generate",
    ),
        path(
        "act/<int:act_id>/delete/",
        views.material_act_delete,
        name="material_act_delete",
    ),
    path(
        "material-document/<int:document_id>/download/",
        views.material_document_download,
        name="material_document_download",
    ),
    path(
        "normative-document/<int:document_id>/download/",
        views.normative_document_download,
        name="normative_document_download",
    ),
]


# ==================================================
# MEDIA-ФАЙЛЫ В РЕЖИМЕ РАЗРАБОТКИ
# ==================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )