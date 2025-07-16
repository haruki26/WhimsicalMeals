from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """材料管理画面."""

    list_display = ("name", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name", "user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
