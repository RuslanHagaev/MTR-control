from django.contrib import admin

from .models import (
    Object,
    Position,
    ProjectCode,
    Supplier,
    Material,
    MaterialDocument,
    MaterialAct,
    NormativeDocument,
    UserProfile,
    AuditLog,
)


# ============================================================
# ОБЪЕКТЫ
# ============================================================

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )

    search_fields = (
        "name",
    )


# ============================================================
# ПОЗИЦИИ
# ============================================================

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "object",
    )

    list_filter = (
        "object",
    )

    search_fields = (
        "name",
        "object__name",
    )


# ============================================================
# ШИФРЫ ПРОЕКТА
# ============================================================

@admin.register(ProjectCode)
class ProjectCodeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "position",
    )

    list_filter = (
        "position",
    )

    search_fields = (
        "code",
        "position__name",
        "position__object__name",
    )


# ============================================================
# ПОСТАВЩИКИ
# ============================================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ============================================================
# МАТЕРИАЛЫ
# ============================================================

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "project_code",
        "supplier",
        "quantity",
        "unit",
        "status",
        "note_level",
    )

    list_filter = (
        "status",
        "note_level",
        "unit",
        "supplier",
    )

    search_fields = (
        "name",
        "project_code__code",
        "project_code__position__name",
        "project_code__position__object__name",
        "supplier__name",
    )

    list_select_related = (
        "project_code",
        "project_code__position",
        "project_code__position__object",
        "supplier",
    )


# ============================================================
# ДОКУМЕНТЫ МАТЕРИАЛОВ
# ============================================================

@admin.register(MaterialDocument)
class MaterialDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "material",
        "document_type",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
    )

    search_fields = (
        "name",
        "material__name",
    )


# ============================================================
# АоРПИ
# ============================================================

@admin.register(MaterialAct)
class MaterialActAdmin(admin.ModelAdmin):

    list_display = (
        "number",
        "material",
        "date",
        "status",
        "inspection_type",
        "created_at",
    )

    list_filter = (
        "status",
        "inspection_type",
    )

    search_fields = (
        "number",
        "material__name",
        "object_name",
        "position_name",
        "project_code",
    )

    list_select_related = (
        "material",
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
    )

    list_filter = (
        "role",
    )

    filter_horizontal = (
        "allowed_objects",
    )

# ============================================================
# НОРМАТИВНЫЕ ДОКУМЕНТЫ
# ============================================================

@admin.register(NormativeDocument)
class NormativeDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "designation",
        "title",
        "document_type",
        "year",
        "created_at",
    )

    list_filter = (
        "document_type",
        "year",
    )

    search_fields = (
        "designation",
        "title",
        "description",
    )

    ordering = (
        "document_type",
        "designation",
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "created_at",
        "user",
        "action",
        "object_type",
        "object_name",
        "description",
    )

    list_filter = (
        "action",
        "object_type",
        "created_at",
    )

    search_fields = (
        "user__username",
        "object_type",
        "object_name",
        "description",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "user",
        "action",
        "object_type",
        "object_id",
        "object_name",
        "description",
        "created_at",
    )