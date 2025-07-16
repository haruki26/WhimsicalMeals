"""料理生成関連のフォーム."""

from typing import Any, ClassVar

from django import forms

from .models import GeneratedDish


class DishGenerationForm(forms.Form):
    """料理名生成フォーム(材料選択なし、ボタンのみ)."""

    # このフォームは実際の入力フィールドは持たず、
    # CSRFトークンの送信とPOSTリクエストの処理のためのみ使用


class SaveDishForm(forms.ModelForm):
    """生成された料理を保存するフォーム."""

    class Meta:
        model = GeneratedDish
        fields: ClassVar[list[str]] = ["name"]
        widgets: ClassVar[dict] = {
            "name": forms.HiddenInput(),
        }

    def __init__(self, user: Any, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """フォーム初期化時にユーザーを設定."""
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> GeneratedDish:  # noqa: FBT001, FBT002
        """保存時にユーザーを設定."""
        dish = super().save(commit=False)
        dish.user = self.user
        if commit:
            dish.save()
        return dish
