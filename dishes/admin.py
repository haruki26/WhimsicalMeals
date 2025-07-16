from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import GeneratedDish, Like


@admin.register(GeneratedDish)
class GeneratedDishAdmin(admin.ModelAdmin):
    """生成料理の管理画面."""

    list_display = ("name", "user", "likes_count", "created_at")
    list_filter = ("created_at", "likes_count")
    search_fields = ("name", "user__username")
    readonly_fields = ("created_at", "likes_count")
    filter_horizontal = ("ingredients",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[GeneratedDish]:
        """関連オブジェクトを効率的に取得."""
        return (
            super()
            .get_queryset(request)
            .select_related("user")
            .prefetch_related(
                "ingredients",
            )
        )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """いいねの管理画面."""

    list_display = ("user", "dish", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "dish__name")
    readonly_fields = ("created_at",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Like]:
        """関連オブジェクトを効率的に取得."""
        return super().get_queryset(request).select_related("user", "dish")
