from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden
from django.db.models import Q
from .document_generator import generate_material_act

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

from .forms import (
    MaterialForm,
    MaterialDocumentForm,
    PositionForm,
    ProjectCodeForm,
    MaterialActForm,
)

from .permissions import (
    is_admin,
    can_view_object,
    can_edit_object,
    can_view_position,
    can_edit_position,
    can_view_project_code,
    can_edit_project_code,
    can_view_material,
    can_edit_material,
    can_view_document,
    can_edit_document,
    can_view_act,
    can_edit_act,
)
from django.contrib.auth.models import User


def can_view_audit_log(user):

    if not user.is_authenticated:
        return False

    try:
        role = user.profile.role
    except UserProfile.DoesNotExist:
        return False

    return role in (
        UserProfile.Role.ADMIN,
        UserProfile.Role.MANAGEMENT,
    )

def audit_log(request):

    if not can_view_audit_log(request.user):
        return HttpResponseForbidden(
            "У вас нет доступа к истории изменений."
        )

    logs = AuditLog.objects.select_related(
        "user"
    ).order_by("-created_at")

    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    selected_user = request.GET.get("user", "").strip()
    selected_action = request.GET.get("action", "").strip()
    selected_object_type = request.GET.get("object_type", "").strip()

    if date_from:
        logs = logs.filter(
            created_at__date__gte=date_from
        )

    if date_to:
        logs = logs.filter(
            created_at__date__lte=date_to
        )

    if selected_user:
        logs = logs.filter(
            user_id=selected_user
        )

    if selected_action:
        logs = logs.filter(
            action=selected_action
        )

    if selected_object_type:
        logs = logs.filter(
            object_type=selected_object_type
        )

    users = User.objects.filter(
        audit_logs__isnull=False
    ).distinct().order_by("username")

    object_types = (
        AuditLog.objects
        .values_list(
            "object_type",
            flat=True
        )
        .distinct()
        .order_by("object_type")
    )

    context = {
        "logs": logs,
        "users": users,
        "object_types": object_types,
        "date_from": date_from,
        "date_to": date_to,
        "selected_user": selected_user,
        "selected_action": selected_action,
        "selected_object_type": selected_object_type,
        "action_choices": AuditLog.Action.choices,
    }

    return render(
        request,
        "core/audit_log.html",
        context,
    )

def permission_denied(request, message):
    return render(
        request,
        "core/403.html",
        {
            "message": message,
        },
        status=403,
    )
# ============================================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================================

def home(request):

    if request.user.is_authenticated and hasattr(
        request.user,
        "profile"
    ):

        if is_admin(request.user):

            objects = Object.objects.all()

        else:

            objects = request.user.profile.allowed_objects.all()

    else:
        objects = Object.objects.none()
   

    total_objects = objects.count()

# --------------------------------------------------------
# МТР и позиции только доступных пользователю объектов
# --------------------------------------------------------

    positions = Position.objects.filter(
        object__in=objects
    )

    materials = Material.objects.filter(
        project_code__position__object__in=objects
    )

    total_positions = positions.count()

    total_materials = materials.count()

    received_materials = materials.filter(
            status=Material.Status.RECEIVED
        ).count()

    checking_materials = materials.filter(
        status=Material.Status.CHECKING
    ).count()

    warning_materials = materials.filter(
        status=Material.Status.WARNING
    ).count()

    accepted_materials = materials.filter(
        status=Material.Status.ACCEPTED
    ).count()

    rejected_materials = materials.filter(
        status=Material.Status.REJECTED
    ).count()

    # --------------------------------------------------------
    # Проценты для диаграммы
    # --------------------------------------------------------

    if total_materials > 0:

        received_percent = round(
            received_materials / total_materials * 100,
            2
        )

        checking_percent = round(
            checking_materials / total_materials * 100,
            2
        )

        warning_percent = round(
            warning_materials / total_materials * 100,
            2
        )

        accepted_percent = round(
            accepted_materials / total_materials * 100,
            2
        )

        rejected_percent = round(
            rejected_materials / total_materials * 100,
            2
        )

    else:

        received_percent = 0
        checking_percent = 0
        warning_percent = 0
        accepted_percent = 0
        rejected_percent = 0

    context = {

        "objects": objects,

        "total_objects": total_objects,

        "total_positions": total_positions,

        "total_materials": total_materials,

        "checking_materials": checking_materials,

        "warning_materials": warning_materials,

        "received_materials": received_materials,

        "accepted_materials": accepted_materials,

        "rejected_materials": rejected_materials,

        "received_percent": received_percent,

        "checking_percent": checking_percent,

        "warning_percent": warning_percent,

        "accepted_percent": accepted_percent,

        "rejected_percent": rejected_percent,

    }

    return render(
        request,
        "core/home.html",
        context
    )
# ============================================================
# ПЕРЕКЛЮЧЕНИЕ РАСКЛАДКИ КЛАВИАТУРЫ
# ============================================================
# ============================================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ============================================================

def profile(request):

    if not request.user.is_authenticated:

        return redirect("login")

    if not hasattr(request.user, "profile"):

        return permission_denied(
            request,
            "Профиль пользователя не настроен."
        )

    profile = request.user.profile

    allowed_objects = profile.allowed_objects.all()

    return render(
        request,
        "core/profile.html",
        {
            "profile": profile,
            "allowed_objects": allowed_objects,
        }
    )
def convert_keyboard_layout(text):

    ru_to_en = {
        "й": "q",
        "ц": "w",
        "у": "e",
        "к": "r",
        "е": "t",
        "н": "y",
        "г": "u",
        "ш": "i",
        "щ": "o",
        "з": "p",
        "х": "[",
        "ъ": "]",
        "ф": "a",
        "ы": "s",
        "в": "d",
        "а": "f",
        "п": "g",
        "р": "h",
        "о": "j",
        "л": "k",
        "д": "l",
        "ж": ";",
        "э": "'",
        "я": "z",
        "ч": "x",
        "с": "c",
        "м": "v",
        "и": "b",
        "т": "n",
        "ь": "m",
        "б": ",",
        "ю": ".",
    }

    en_to_ru = {
        value: key
        for key, value in ru_to_en.items()
    }

    def translate(text, mapping):

        result = ""

        for char in text:

            lower_char = char.lower()

            if lower_char in mapping:

                translated = mapping[lower_char]

                if char.isupper():
                    translated = translated.upper()

                result += translated

            else:

                result += char

        return result

    return (
        translate(text, ru_to_en),
        translate(text, en_to_ru),
    )

# ============================================================
# ПЕРЕКЛЮЧЕНИЕ РАСКЛАДКИ
# ============================================================

def convert_keyboard_layout(text):

    ru_to_en = str.maketrans(
        "йцукенгшщзхъфывапролджэячсмитьбю",
        "qwertyuiop[]asdfghjkl;'zxcvbnm,."
    )

    en_to_ru = str.maketrans(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,.",
        "йцукенгшщзхъфывапролджэячсмитьбю"
    )

    return (
        text.translate(ru_to_en),
        text.translate(en_to_ru),
    )


# ============================================================
# ПОИСК
# ============================================================

def search(request):
    if request.user.is_authenticated and hasattr(
        request.user,
        "profile"
    ):
        if is_admin(request.user):
            allowed_objects = Object.objects.all()
        else:
            allowed_objects = request.user.profile.allowed_objects.all()
    else:
        allowed_objects = Object.objects.none()

    query = request.GET.get("q", "").strip()

    objects = []
    positions = []
    project_codes = []
    materials = []
    suppliers = []

    if query:

        # ----------------------------------------------------
        # Делаем поиск независимым от регистра
        # ----------------------------------------------------

        search_text = query.casefold()

        # ----------------------------------------------------
        # Варианты раскладки
        # ----------------------------------------------------

        ru_variant, en_variant = convert_keyboard_layout(
            search_text
        )

        search_variants = {
            search_text,
            ru_variant.casefold(),
            en_variant.casefold(),
        }

        # ----------------------------------------------------
        # ОБЪЕКТЫ
        # ----------------------------------------------------

        for obj in allowed_objects:

            values = [
                obj.name,
                obj.description,
            ]

            if any(
                variant in (
                    value.casefold()
                    if value
                    else ""
                )
                for variant in search_variants
                for value in values
            ):

                objects.append(obj)

        # ----------------------------------------------------
        # ПОЗИЦИИ
        # ----------------------------------------------------

        for position in Position.objects.filter(
            object__in=allowed_objects
        ).select_related(
            "object"
        ):

            values = [
                position.name,
                position.object.name,
            ]

            if any(
                variant in (
                    value.casefold()
                    if value
                    else ""
                )
                for variant in search_variants
                for value in values
            ):

                positions.append(position)

        # ----------------------------------------------------
        # ШИФРЫ ПРОЕКТОВ
        # ----------------------------------------------------

        for project_code in ProjectCode.objects.filter(
            position__object__in=allowed_objects
        ).select_related(
            "position",
            "position__object"
        ):

            values = [
                project_code.code,
                project_code.position.name,
                project_code.position.object.name,
            ]

            if any(
                variant in (
                    value.casefold()
                    if value
                    else ""
                )
                for variant in search_variants
                for value in values
            ):

                project_codes.append(project_code)

        # ----------------------------------------------------
        # ПОСТАВЩИКИ
        # ----------------------------------------------------

        allowed_supplier_ids = Material.objects.filter(
            project_code__position__object__in=allowed_objects
        ).values_list(
            "supplier_id",
            flat=True
        ).distinct()

        for supplier in Supplier.objects.filter(
            id__in=allowed_supplier_ids
        ):

            values = [
                supplier.name,
            ]

            if any(
                variant in (
                    value.casefold()
                    if value
                    else ""
                )
                for variant in search_variants
                for value in values
            ):

                suppliers.append(supplier)

        # ----------------------------------------------------
        # МТР
        # ----------------------------------------------------

        for material in Material.objects.filter(
            project_code__position__object__in=allowed_objects
        ).select_related(
            "supplier",
            "project_code",
            "project_code__position",
            "project_code__position__object",
        ):

            supplier_name = ""

            if material.supplier:

                supplier_name = (
                    material.supplier.name
                )

            values = [
                material.name,
                material.note,
                supplier_name,
                material.project_code.code,
                material.project_code.position.name,
                material.project_code.position.object.name,
            ]

            if any(
                variant in (
                    value.casefold()
                    if value
                    else ""
                )
                for variant in search_variants
                for value in values
            ):

                materials.append(material)

    # --------------------------------------------------------
    # ОБЩЕЕ КОЛИЧЕСТВО
    # --------------------------------------------------------

    total_results = (
        len(objects)
        + len(positions)
        + len(project_codes)
        + len(materials)
        + len(suppliers)
    )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {

        "query": query,

        "objects": objects,

        "positions": positions,

        "project_codes": project_codes,

        "materials": materials,

        "suppliers": suppliers,

        "total_results": total_results,
    }

    return render(
        request,
        "core/search.html",
        context
    )

# ============================================================
# СПИСОК МТР ПО СТАТУСУ
# ============================================================

def material_status_list(request, status):

    allowed_statuses = {
        Material.Status.RECEIVED,
        Material.Status.CHECKING,
        Material.Status.WARNING,
        Material.Status.ACCEPTED,
        Material.Status.REJECTED,
    }

    if status not in allowed_statuses:
        return redirect("home")

    if request.user.is_authenticated and hasattr(
        request.user,
        "profile"
    ):
        if is_admin(request.user):
            allowed_objects = Object.objects.all()
        else:
            allowed_objects = request.user.profile.allowed_objects.all()
    else:
        allowed_objects = Object.objects.none()

    materials = (
        Material.objects
        .filter(
            status=status,
            project_code__position__object__in=allowed_objects
        )
        .select_related(
            "project_code",
            "project_code__position",
            "project_code__position__object",
            "supplier",
        )
    )

    status_names = {
        Material.Status.RECEIVED: "Полученные МТР",
        Material.Status.CHECKING: "МТР на проверке",
        Material.Status.WARNING: "МТР с замечаниями",
        Material.Status.ACCEPTED: "Принятые МТР",
        Material.Status.REJECTED: "Отклонённые МТР",
    }

    return render(
        request,
        "core/material_status_list.html",
        {
            "materials": materials,
            "status": status,
            "status_name": status_names.get(
                status,
                "Материалы"
            ),
        }
    )
# ============================================================
# ОБЪЕКТ
# ============================================================

def object_detail(request, object_id):

    obj = get_object_or_404(
        Object,
        id=object_id
    )

    if not can_view_object(
        request.user,
        obj
    ):

        return permission_denied(
            request,
            "У вас нет доступа к этому объекту."
        )

    positions = obj.positions.all()

    return render(
        request,
        "core/object_detail.html",
        {
            "object": obj,
            "positions": positions,
        }
    )
# ============================================================
# ДОБАВЛЕНИЕ ПОЗИЦИИ
# ============================================================

def position_create(request, object_id):

    obj = get_object_or_404(
        Object,
        id=object_id
    )

    if not can_edit_object(
        request.user,
        obj
    ):

        return permission_denied(
            request,
            "У вас нет прав на изменение этого объекта."
        )

    if request.method == "POST":

        form = PositionForm(request.POST)

        if form.is_valid():

            position = form.save(
                commit=False
            )

            position.object = obj

            position.save()

            return redirect(
                "object_detail",
                object_id=obj.id
            )

    else:

        form = PositionForm()

    return render(
        request,
        "core/position_form.html",
        {
            "form": form,
            "object": obj,
        }
    )
# ============================================================
# ПОЗИЦИЯ
# ============================================================

def position_detail(request, position_id):

    position = get_object_or_404(
        Position,
        id=position_id
    )

    if not can_view_position(
        request.user,
        position
    ):

        return permission_denied(
            request,
            "У вас нет доступа к этой позиции."
        )

    project_codes = position.project_codes.all()

    return render(
        request,
        "core/position_detail.html",
        {
            "position": position,
            "project_codes": project_codes,
        }
    )

# ============================================================
# ДОБАВЛЕНИЕ ШИФРА
# ============================================================

def project_code_create(request, position_id):

    position = get_object_or_404(
        Position,
        id=position_id
    )
    if not can_edit_position(
        request.user,
        position
    ):
        return permission_denied(
            request,
            "У вас нет прав на изменение этой позиции."
        )

    if request.method == "POST":

        form = ProjectCodeForm(request.POST)

        if form.is_valid():

            project_code = form.save(commit=False)

            project_code.position = position

            project_code.save()

            return redirect(
                "position_detail",
                position_id=position.id
            )

    else:

        form = ProjectCodeForm()

    return render(
        request,
        "core/project_code_form.html",
        {
            "form": form,
            "position": position,
        }
    )


# ============================================================
# ШИФР
# ============================================================

def project_code_detail(request, project_code_id):

    project_code = get_object_or_404(
        ProjectCode,
        id=project_code_id
    )

    if not can_view_project_code(
        request.user,
        project_code
    ):
        return permission_denied(
            request,
            "У вас нет доступа к этому шифру проекта."
        )

    materials = project_code.materials.all()

    return render(
        request,
        "core/project_code_detail.html",
        {
            "project_code": project_code,
            "materials": materials,
        }
    )


# ============================================================
# ДОБАВЛЕНИЕ МАТЕРИАЛА
# ============================================================

def material_create(request, project_code_id):

    project_code = get_object_or_404(
        ProjectCode,
        id=project_code_id
    )
    if not can_edit_project_code(
        request.user,
        project_code
    ):
        return permission_denied(
            request,
            "У вас нет прав на изменение этого шифра."
        )
    if request.method == "POST":

        form = MaterialForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            material = form.save(
                commit=False
            )

            material.project_code = project_code

            material.save()

            return redirect(
                "project_code_detail",
                project_code_id=project_code.id
            )

    else:

        form = MaterialForm()

    return render(
        request,
        "core/material_form.html",
        {
            "form": form,
            "project_code": project_code,
        }
    )


# ============================================================
# ПРОСМОТР МАТЕРИАЛА
# ============================================================

def material_detail(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )
    if not can_view_material(
        request.user,
        material
    ):
        return permission_denied(
            request,
            "У вас нет доступа к этому МТР."
        )
    documents = material.documents.all()

    return render(
        request,
        "core/material_detail.html",
        {
            "material": material,
            "documents": documents,
        }
    )


# ============================================================
# РЕДАКТИРОВАНИЕ МАТЕРИАЛА
# ============================================================

def material_edit(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )
    if not can_edit_material(
        request.user,
        material
    ):
        return permission_denied(
            request,
            "У вас нет прав на изменение этого МТР."
        )
    if request.method == "POST":

        form = MaterialForm(
            request.POST,
            request.FILES,
            instance=material
        )

        if form.is_valid():

            form.save()

            return redirect(
                "project_code_detail",
                project_code_id=material.project_code.id
            )

    else:

        form = MaterialForm(
            instance=material
        )

    return render(
        request,
        "core/material_form.html",
        {
            "form": form,
            "project_code": material.project_code,
            "material": material,
        }
    )


# ============================================================
# УДАЛЕНИЕ МАТЕРИАЛА
# ============================================================

def material_delete(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )
    if not can_edit_material(
        request.user,
        material
    ):
        return permission_denied(
            request,
            "У вас нет прав на удаление этого МТР."
        )
    project_code_id = material.project_code.id

    if request.method == "POST":

        material.delete()

        return redirect(
            "project_code_detail",
            project_code_id=project_code_id
        )

    return render(
        request,
        "core/material_confirm_delete.html",
        {
            "material": material,
            "project_code": material.project_code,
        }
    )


# ============================================================
# ДОКУМЕНТЫ МАТЕРИАЛА
# ============================================================

def material_documents(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )
    if not can_view_material(
        request.user,
        material
    ):
        return permission_denied(
            request,
            "У вас нет доступа к документам этого МТР."
        )
    project_code = material.project_code
    position = project_code.position
    obj = position.object

    if request.method == "POST":

        if not can_edit_material(
            request.user,
            material
        ):
                return permission_denied(
                    request,
                    "У вас нет прав на загрузку документов."
                    "Ваша роль позволяет только просмотр документов."
                )

        document_type = request.POST.get(
            "document_type"
        )

        files = request.FILES.getlist(
            "files"
        )

        for uploaded_file in files:

            MaterialDocument.objects.create(
                material=material,
                document_type=document_type,
                name=uploaded_file.name,
                file=uploaded_file
            )

        return redirect(
            "material_documents",
            material_id=material.id
        )

    documents = material.documents.all()

    document_form = MaterialDocumentForm()

    return render(
        request,
        "core/material_documents.html",
        {
            "material": material,
            "documents": documents,
            "document_form": document_form,
            "project_code": project_code,
            "position": position,
            "object": obj,
        }
    )


# ============================================================
# УДАЛЕНИЕ ДОКУМЕНТА
# ============================================================

def material_document_delete(
    request,
    document_id
):

    document = get_object_or_404(
        MaterialDocument,
        id=document_id
    )
    if not can_edit_document(
        request.user,
        document
    ):
        return permission_denied(
            request,
            "У вас нет прав на удаление этого документа."
        )
    material_id = document.material.id

    if request.method == "POST":

        if document.file:

            document.file.delete(
                save=False
            )

        document.delete()

        return redirect(
            "material_documents",
            material_id=material_id
        )

    return render(
        request,
        "core/material_document_confirm_delete.html",
        {
            "document": document,
            "material": document.material,
            "material_id": material_id,
        }
    )


# ============================================================
# СОЗДАНИЕ АоРПИ
# ============================================================

def material_act_create(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id
    )
    if not can_edit_material(
        request.user,
        material
    ):
        return permission_denied(
            request,
            "У вас нет прав на создание АоРПИ."
        )
    project_code = material.project_code
    position = project_code.position
    obj = position.object

    if request.method == "POST":

        form = MaterialActForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            act = form.save(
                commit=False
            )

            act.material = material

            act.save()

            return redirect(
                "material_act_detail",
                act_id=act.id
            )

    else:

        form = MaterialActForm(
            initial={
                "customer": "",
                "contractor": "",

                "object_name": obj.name,
                "position_name": position.name,
                "project_code": project_code.code,

                "product_name": material.name,

                "status": MaterialAct.ActStatus.DRAFT,

                "inspection_type": (
                    MaterialAct.InspectionType.CONTINUOUS
                ),

                "documents_complete": True,
            }
        )

    return render(
        request,
        "core/material_act_form.html",
        {
            "form": form,
            "material": material,
            "project_code": project_code,
            "position": position,
            "object": obj,
        }
    )


# ============================================================
# ПРОСМОТР АоРПИ
# ============================================================

def material_act_detail(request, act_id):

    act = get_object_or_404(
        MaterialAct,
        id=act_id
    )
    if not can_view_act(
        request.user,
        act
    ):
        return permission_denied(
            request,
            "У вас нет доступа к этому АоРПИ."
        )
    return render(
        request,
        "core/material_act_detail.html",
        {
            "act": act,
        }
    )


# ============================================================
# РЕДАКТИРОВАНИЕ АоРПИ
# ============================================================

def material_act_edit(request, act_id):

    act = get_object_or_404(
        MaterialAct,
        id=act_id
    )
    if not can_edit_act(
        request.user,
        act
    ):
        return permission_denied(
            request,
            "У вас нет прав на редактирование этого АоРПИ."
        )
    if request.method == "POST":

        form = MaterialActForm(
            request.POST,
            request.FILES,
            instance=act
        )

        if form.is_valid():

            form.save()

            return redirect(
                "material_act_detail",
                act_id=act.id
            )

    else:

        form = MaterialActForm(
            instance=act
        )

    return render(
        request,
        "core/material_act_form.html",
        {
            "form": form,
            "material": act.material,
            "act": act,
        }
    )


# ============================================================
# УДАЛЕНИЕ АоРПИ
# ============================================================

def material_act_delete(request, act_id):

    act = get_object_or_404(
        MaterialAct,
        id=act_id
    )
    if not can_edit_act(
        request.user,
        act
    ):
        return permission_denied(
            request,
            "У вас нет прав на удаление этого АоРПИ."
        )
    material_id = act.material.id
    project_code_id = act.material.project_code.id

    if request.method == "POST":

        if act.signed_file:

            act.signed_file.delete(
                save=False
            )

        act.delete()

        return redirect(
            "project_code_detail",
            project_code_id=project_code_id
        )

    return render(
        request,
        "core/material_act_confirm_delete.html",
        {
            "act": act,
            "material": act.material,
            "material_id": material_id,
        }
    )


# ============================================================
# ФОРМИРОВАНИЕ АоРПИ В WORD
# ============================================================

# ============================================================
# ФОРМИРОВАНИЕ АоРПИ В WORD
# ============================================================

def material_act_generate(request, act_id):

    act = get_object_or_404(
        MaterialAct,
        id=act_id
    )

    if not can_view_act(
        request.user,
        act
    ):
        return permission_denied(
            request,
            "У вас нет доступа к этому АоРПИ."
        )

    document = generate_material_act(act)

    filename = (
        f"АоРПИ_"
        f"{act.number or act.id}.docx"
    )

    response = FileResponse(
        document,
        as_attachment=True,
        filename=filename
    )

    return response

# ============================================================
# НОРМАТИВНЫЕ ДОКУМЕНТЫ — СПИСОК
# ============================================================

def normative_documents(request):

    documents = NormativeDocument.objects.all()

    query = request.GET.get(
        "q",
        ""
    ).strip()

    if query:
        documents = documents.filter(
            Q(
                designation__icontains=query
            )
            |
            Q(
                title__icontains=query
            )
            |
            Q(
                description__icontains=query
            )
        )

    return render(
        request,
        "core/normative_documents.html",
        {
            "documents": documents,
            "query": query,
        }
    )


# ============================================================
# НОРМАТИВНЫЙ ДОКУМЕНТ — ПРОСМОТР
# ============================================================

def normative_document_detail(
    request,
    document_id
):

    document = get_object_or_404(
        NormativeDocument,
        id=document_id
    )

    return render(
        request,
        "core/normative_document_detail.html",
        {
            "document": document,
        }
    )

