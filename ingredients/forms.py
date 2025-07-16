from typing import Any, ClassVar

from django import forms
from django.contrib.auth.models import User

from .models import Ingredient


class IngredientForm(forms.ModelForm):
    """材料登録・編集フォーム."""

    class Meta:
        model = Ingredient
        fields: ClassVar[list[str]] = ["name"]
        widgets: ClassVar[dict] = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "材料名を入力してください (例: 卵、ネギ、チーズ)",
                    "class": "form-control",
                    "maxlength": "100",
                },
            ),
        }

    def __init__(self, user: User, *args: Any, **kwargs: object) -> None:  # noqa: ANN401
        """フォーム初期化時にユーザーを設定."""
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_name(self) -> str | None:
        """材料名の重複チェック."""
        name = self.cleaned_data.get("name")
        if name:
            # 編集時は自分自身を除外して重複チェック
            existing_ingredients = Ingredient.objects.filter(
                user=self.user,
                name__iexact=name,
            )
            if self.instance.pk:
                existing_ingredients = existing_ingredients.exclude(pk=self.instance.pk)

            if existing_ingredients.exists():
                msg = f"「{name}」は既に登録されています。"
                raise forms.ValidationError(msg)

        return name

    def save(self, commit: bool = True) -> Ingredient:  # noqa: FBT001, FBT002
        """保存時にユーザーを設定."""
        ingredient = super().save(commit=False)
        ingredient.user = self.user
        if commit:
            ingredient.save()
        return ingredient
