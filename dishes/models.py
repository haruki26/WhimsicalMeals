from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ingredients.models import Ingredient


class GeneratedDish(models.Model):
    """生成された架空料理モデル."""

    name = models.CharField(
        max_length=200,
        verbose_name="料理名",
        help_text="生成された架空料理の名前",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="作成ユーザー",
        related_name="generated_dishes",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="使用材料",
        related_name="dishes",
        help_text="この料理に使用された材料",
    )
    likes_count = models.IntegerField(
        default=0,
        verbose_name="いいね数",
        help_text="この料理に付けられたいいねの数",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日時",
    )

    class Meta:
        verbose_name = "生成料理"
        verbose_name_plural = "生成料理"
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} (by {self.user.username})"


class Like(models.Model):
    """いいねモデル."""

    dish = models.ForeignKey(
        GeneratedDish,
        on_delete=models.CASCADE,
        verbose_name="対象料理",
        related_name="likes",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="いいねしたユーザー",
        related_name="likes",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="いいね日時",
    )

    class Meta:
        # 同じユーザーが同じ料理に複数回いいねできないようにする
        unique_together: ClassVar[list[str]] = ["dish", "user"]
        verbose_name = "いいね"
        verbose_name_plural = "いいね"
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} → {self.dish.name}"


# いいねが追加・削除された時にlikes_countを自動更新
@receiver(post_save, sender=Like)
def update_likes_count_on_add(
    *,
    instance: Like,
    created: bool,
    **_kwargs: object,
) -> None:
    """いいね追加時にlikes_countを更新."""
    if created:
        instance.dish.likes_count = instance.dish.likes.count()  # type: ignore[attr-defined]
        instance.dish.save(update_fields=["likes_count"])


@receiver(post_delete, sender=Like)
def update_likes_count_on_delete(
    *,
    instance: Like,
    **_kwargs: object,
) -> None:
    """いいね削除時にlikes_countを更新."""
    instance.dish.likes_count = instance.dish.likes.count()  # type: ignore[attr-defined]
    instance.dish.save(update_fields=["likes_count"])
