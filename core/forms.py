from django import forms

from .models import (
    Material,
    MaterialDocument,
    MaterialAct,
    Position,
    ProjectCode,
)


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position

        fields = [
            "name",
        ]

        labels = {
            "name": "Название позиции",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Введите название позиции",
                }
            ),
        }


class ProjectCodeForm(forms.ModelForm):

    class Meta:
        model = ProjectCode

        fields = [
            "code",
        ]

        labels = {
            "code": "Шифр",
        }

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Введите шифр",
                }
            ),
        }


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material

        fields = [
            "project_code",
            "name",
            "quantity",
            "unit",
            "supplier",
            "status",
            "note_level",
            "note",
        ]

        labels = {
            "project_code": "Шифр проекта",
            "name": "Наименование",
            "quantity": "Количество",
            "unit": "Единица измерения",
            "supplier": "Поставщик",
            "status": "Статус",
            "note_level": "Уровень замечания",
            "note": "Примечание",
        }

        widgets = {
            "note": forms.Textarea(
                attrs={
                    "placeholder": "Опишите замечание...",
                    "rows": 4,
                }
            ),
        }


class MaterialDocumentForm(forms.ModelForm):

    class Meta:
        model = MaterialDocument

        fields = [
            "document_type",
            "file",
        ]

        labels = {
            "document_type": "Тип документа",
            "file": "Файл",
        }


# ============================================================
# АоРПИ
# ============================================================

class MaterialActForm(forms.ModelForm):

    class Meta:
        model = MaterialAct

        fields = [
            "number",
            "date",
            "status",

            "customer",
            "contractor",

            "object_name",
            "position_name",
            "project_code",

            "product_type",
            "inspection_type",
            "product_name",

            "project_document",
            "project_document_date",
            "working_drawings",
            "construction_section",

            "geometric_dimensions",
            "marking",
            "technical_conditions",
            "compliance_result",

            "accompanying_documents",
            "documents_complete",

            "mechanical_properties",
            "mechanical_properties_result",

            "project_requirements",
            "technical_requirements",

            "conclusion",

            "contractor_position",
            "contractor_representative",
            "contractor_signature_date",

            "customer_position",
            "customer_representative",
            "customer_signature_date",

            "signed_file",
        ]

        labels = {
            "number": "№ АоРПИ",
            "date": "Дата акта",
            "status": "Статус",

            "customer": "Заказчик",
            "contractor": "Подрядчик",

            "object_name": "Объект",
            "position_name": "Позиция",
            "project_code": "Шифр проекта",

            "product_type": "Вид изделий",
            "inspection_type": "Вид проверки",
            "product_name": "Наименование изделий",

            "project_document": "Проект / чертёж",
            "project_document_date": "Дата проекта / чертежа",
            "working_drawings": "Рабочие чертежи",
            "construction_section": "Участок / привязка / км / ПК",

            "geometric_dimensions": "Геометрические размеры",
            "marking": "Маркировка",
            "technical_conditions": "Технические условия",
            "compliance_result": "Соответствие",

            "accompanying_documents": "Сопроводительная документация",
            "documents_complete": "Документация в полном комплекте",

            "mechanical_properties": "Характеристики механических свойств",
            "mechanical_properties_result": "Результат проверки механических свойств",

            "project_requirements": "Требования проекта",
            "technical_requirements": "Технические условия",

            "conclusion": "Заключение",

            "contractor_position": "Должность представителя подрядчика",
            "contractor_representative": "Представитель подрядчика",
            "contractor_signature_date": "Дата подписи подрядчика",

            "customer_position": "Должность представителя заказчика",
            "customer_representative": "Представитель заказчика",
            "customer_signature_date": "Дата подписи заказчика",

            "signed_file": "Подписанный АоРПИ",
        }

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "project_document_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "contractor_signature_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "customer_signature_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "geometric_dimensions": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Например: диаметр, толщина стенки, "
                        "угол изгиба и т.д."
                    ),
                }
            ),

            "marking": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Укажите маркировку изделия",
                }
            ),

            "technical_conditions": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Номер и требования ТУ",
                }
            ),

            "accompanying_documents": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Паспорта, сертификаты, декларации "
                        "и другие документы"
                    ),
                }
            ),

            "mechanical_properties": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Данные сопроводительной документации "
                        "или результаты испытаний"
                    ),
                }
            ),

            "mechanical_properties_result": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Результат проверки механических свойств"
                    ),
                }
            ),

            "project_requirements": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Требования проекта",
                }
            ),

            "technical_requirements": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Требования технических условий",
                }
            ),

            "conclusion": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": (
                        "Итоговое заключение по результатам "
                        "входного контроля"
                    ),
                }
            ),
        }