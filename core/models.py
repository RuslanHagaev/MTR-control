from django.db import models
from django.contrib.auth.models import User

class Object(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        related_name="positions"
    )

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class ProjectCode(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="project_codes"
    )

    code = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.code


class Supplier(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name


class Material(models.Model):

    class Status(models.TextChoices):
        RECEIVED = "received", "Получен"
        CHECKING = "checking", "На проверке"
        WARNING = "warning", "Есть замечания"
        ACCEPTED = "accepted", "Принят"
        REJECTED = "rejected", "Отклонён"

    class NoteLevel(models.TextChoices):
        NONE = "none", "Нет замечаний"
        LOW = "low", "Лёгкое"
        MEDIUM = "medium", "Среднее"
        CRITICAL = "critical", "Критическое"

    class Unit(models.TextChoices):
        PIECE = "шт.", "шт."
        PACKAGE = "упак.", "упак."
        SET = "компл.", "компл."
        METER = "м", "м"
        SQUARE_METER = "м²", "м²"
        CUBIC_METER = "м³", "м³"
        KILOGRAM = "кг", "кг"
        TON = "т", "т"
        LITER = "л", "л"
        LINEAR_METER = "м.п.", "м.п."
        ROLL = "рул.", "рул."
        SHEET = "лист", "лист"
        PAIR = "пара", "пара"
        SECTION = "секция", "секция"
        CAN = "банка", "банка"
        BUCKET = "ведро", "ведро"
        OTHER = "другое", "другое"

    project_code = models.ForeignKey(
        ProjectCode,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    name = models.CharField(
        max_length=200
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=20,
        choices=Unit.choices,
        default=Unit.PIECE
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        related_name="materials",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED
    )

    note_level = models.CharField(
        max_length=20,
        choices=NoteLevel.choices,
        default=NoteLevel.NONE
    )

    note = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class MaterialDocument(models.Model):

    class DocumentType(models.TextChoices):
        PASSPORT = "passport", "Паспорт"
        CERTIFICATE = "certificate", "Сертификат"
        DECLARATION = "declaration", "Декларация"
        QUALITY = "quality", "Сертификат качества"
        PROTOCOL = "protocol", "Протокол испытаний"
        PHOTO = "photo", "Фото"
        OTHER = "other", "Другой документ"

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER
    )

    name = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="material_documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class MaterialAct(models.Model):

    class ActStatus(models.TextChoices):
        DRAFT = "draft", "Разработка"
        SIGNED = "signed", "Подписан"

    class InspectionType(models.TextChoices):
        CONTINUOUS = "continuous", "Сплошной"
        SELECTIVE = "selective", "Выборочный"
        SAMPLE = "sample", "С выборкой"

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="acts"
    )

    # =========================================================
    # ОСНОВНЫЕ ДАННЫЕ АКТА
    # =========================================================

    number = models.CharField(
        "Номер акта",
        max_length=100,
        blank=True
    )

    date = models.DateField(
        "Дата акта",
        null=True,
        blank=True
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=ActStatus.choices,
        default=ActStatus.DRAFT
    )

    # =========================================================
    # ОРГАНИЗАЦИИ
    # =========================================================

    customer = models.CharField(
        "Заказчик",
        max_length=300,
        blank=True
    )

    contractor = models.CharField(
        "Подрядчик",
        max_length=300,
        blank=True
    )

    # =========================================================
    # ОБЪЕКТ / ПОЗИЦИЯ / ШИФР
    # =========================================================

    object_name = models.CharField(
        "Объект",
        max_length=300,
        blank=True
    )

    position_name = models.CharField(
        "Позиция",
        max_length=300,
        blank=True
    )

    project_code = models.CharField(
        "Шифр проекта",
        max_length=300,
        blank=True
    )

    # =========================================================
    # ИЗДЕЛИЯ
    # =========================================================

    product_type = models.CharField(
        "Вид изделий",
        max_length=500,
        blank=True
    )

    inspection_type = models.CharField(
        "Вид проверки",
        max_length=30,
        choices=InspectionType.choices,
        default=InspectionType.CONTINUOUS
    )

    product_name = models.CharField(
        "Наименование изделий",
        max_length=500,
        blank=True
    )

    # =========================================================
    # ПРОЕКТ / ЧЕРТЁЖ
    # =========================================================

    project_document = models.CharField(
        "Проект / чертёж",
        max_length=500,
        blank=True
    )

    project_document_date = models.DateField(
        "Дата проекта / чертежа",
        null=True,
        blank=True
    )

    # =========================================================
    # УЧАСТОК
    # =========================================================

    construction_section = models.CharField(
        "Участок / привязка / км / ПК",
        max_length=500,
        blank=True
    )

    # =========================================================
    # РЕЗУЛЬТАТЫ ПРОВЕРКИ
    # =========================================================

    geometric_dimensions = models.TextField(
        "Геометрические размеры",
        blank=True
    )

    marking = models.TextField(
        "Маркировка",
        blank=True
    )

    technical_conditions = models.TextField(
        "Технические условия",
        blank=True
    )

    compliance_result = models.CharField(
        "Соответствие",
        max_length=50,
        blank=True
    )

    working_drawings = models.CharField(
        "Рабочие чертежи",
        max_length=500,
        blank=True
    )

    # =========================================================
    # СОПРОВОДИТЕЛЬНАЯ ДОКУМЕНТАЦИЯ
    # =========================================================

    accompanying_documents = models.TextField(
        "Сопроводительная документация",
        blank=True
    )

    documents_complete = models.BooleanField(
        "Документация в полном комплекте",
        default=True
    )

    # =========================================================
    # МЕХАНИЧЕСКИЕ СВОЙСТВА
    # =========================================================

    mechanical_properties = models.TextField(
        "Характеристики механических свойств",
        blank=True
    )

    mechanical_properties_result = models.TextField(
        "Результат проверки механических свойств",
        blank=True
    )

    # =========================================================
    # ТРЕБОВАНИЯ
    # =========================================================

    project_requirements = models.TextField(
        "Требования проекта",
        blank=True
    )

    technical_requirements = models.TextField(
        "Технические условия",
        blank=True
    )

    conclusion = models.TextField(
        "Заключение",
        blank=True
    )

    # =========================================================
    # ПРЕДСТАВИТЕЛЬ ПОДРЯДЧИКА
    # =========================================================

    contractor_position = models.CharField(
        "Должность представителя подрядчика",
        max_length=300,
        blank=True
    )

    contractor_representative = models.CharField(
        "Представитель подрядчика",
        max_length=300,
        blank=True
    )

    contractor_signature_date = models.DateField(
        "Дата подписи подрядчика",
        null=True,
        blank=True
    )

    # =========================================================
    # ПРЕДСТАВИТЕЛЬ ЗАКАЗЧИКА
    # =========================================================

    customer_position = models.CharField(
        "Должность представителя заказчика",
        max_length=300,
        blank=True
    )

    customer_representative = models.CharField(
        "Представитель заказчика",
        max_length=300,
        blank=True
    )

    customer_signature_date = models.DateField(
        "Дата подписи заказчика",
        null=True,
        blank=True
    )

    # =========================================================
    # ФАЙЛ ПОДПИСАННОГО АО РПИ
    # =========================================================

    signed_file = models.FileField(
        "Подписанный АоРПИ",
        upload_to="material_acts/",
        blank=True,
        null=True
    )

    # =========================================================
    # СИСТЕМНЫЕ ПОЛЯ
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        if self.number:
            return f"АоРПИ № {self.number}"

        return f"АоРПИ — {self.material.name}"
    
# ============================================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ============================================================

# ============================================================
# НОРМАТИВНЫЕ ДОКУМЕНТЫ
# ============================================================

class NormativeDocument(models.Model):

    class DocumentType(models.TextChoices):
        GOST = "gost", "ГОСТ"
        GOST_R = "gost_r", "ГОСТ Р"
        SP = "sp", "СП"
        SNIP = "snip", "СНиП"
        PUE = "pue", "ПУЭ"
        SANPIN = "sanpin", "СанПиН"
        OTHER = "other", "Другой документ"

    title = models.CharField(
        "Название",
        max_length=500
    )

    designation = models.CharField(
        "Обозначение",
        max_length=100,
        unique=True
    )

    document_type = models.CharField(
        "Тип документа",
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.GOST
    )

    year = models.PositiveIntegerField(
        "Год",
        blank=True,
        null=True
    )

    description = models.TextField(
        "Описание",
        blank=True
    )

    file = models.FileField(
        "Файл документа",
        upload_to="normative_documents/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Дата обновления",
        auto_now=True
    )

    class Meta:
        verbose_name = "Нормативный документ"
        verbose_name_plural = "Нормативные документы"
        ordering = ["document_type", "designation"]

    def __str__(self):
        return f"{self.designation} — {self.title}"


class UserProfile(models.Model):

    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        VKH_ENGINEER = "vkh_engineer", "Инженер ВК"
        LEAD_VKH_ENGINEER = "lead_vkh_engineer", "Ведущий инженер ВК"
        PTO_ENGINEER = "pto_engineer", "Инженер ПТО"
        MANAGEMENT = "management", "Руководство"
        GUEST = "guest", "Гость"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.GUEST,
        verbose_name="Роль",
    )

    allowed_objects = models.ManyToManyField(
        Object,
        blank=True,
        related_name="allowed_users",
        verbose_name="Доступные объекты",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

class AuditLog(models.Model):

    class Action(models.TextChoices):
        CREATE = "create", "Создание"
        UPDATE = "update", "Изменение"
        DELETE = "delete", "Удаление"
        UPLOAD = "upload", "Загрузка файла"
        SIGN = "sign", "Подписание"
        OTHER = "other", "Другое"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Пользователь",
    )

    action = models.CharField(
        "Действие",
        max_length=20,
        choices=Action.choices,
    )

    object_type = models.CharField(
        "Тип объекта",
        max_length=100,
    )

    object_id = models.PositiveIntegerField(
        "ID объекта",
        null=True,
        blank=True,
    )

    object_name = models.CharField(
        "Название объекта",
        max_length=500,
        blank=True,
    )

    description = models.TextField(
        "Описание",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Дата и время",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Запись истории"
        verbose_name_plural = "История изменений"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%d.%m.%Y %H:%M} — {self.object_name}"