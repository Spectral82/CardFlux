from django import forms

from .models import Product


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


def validate_forbidden_words(value: str, field_label: str) -> None:
    """Проверяет текст на запрещённые слова без учёта регистра."""
    lowered = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            raise forms.ValidationError(
                f'В поле «{field_label}» обнаружено запрещённое слово: «{word}». '
                f'Переформулируйте текст, пожалуйста.'
            )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "price", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label

    def clean_name(self):
        name = self.cleaned_data["name"]
        validate_forbidden_words(name, "Название")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        validate_forbidden_words(description, "Описание")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. "
                "Введите неотрицательное значение, например 0 или 199.99."
            )
        return price
