from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models


class Ingredient(models.Model):
    """材料モデル."""

    name = models.CharField(
        max_length=100,
        verbose_name="材料名",
        help_text="材料の名前を入力してください (例: 卵、ネギ、チーズ)",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="登録ユーザー",
        related_name="ingredients",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="登録日時",
    )

    class Meta:
        # 同じユーザーが同じ材料名を重複登録できないようにする
        unique_together: ClassVar[list[str]] = ["name", "user"]
        verbose_name = "材料"
        verbose_name_plural = "材料"
        ordering: ClassVar[list[str]] = ["-created_at"]  # 新しい材料から順に表示

    def __str__(self) -> str:
        return f"{self.name} ({self.user.username})"
