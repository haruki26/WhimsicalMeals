from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import IngredientForm
from .models import Ingredient


class IngredientListView(LoginRequiredMixin, ListView):
    """材料一覧表示ビュー."""

    model = Ingredient
    template_name = "ingredients/list.html"
    context_object_name = "ingredients"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Ingredient]:
        """ログインユーザーの材料のみを取得."""
        return Ingredient.objects.filter(user=self.request.user)


class IngredientCreateView(LoginRequiredMixin, CreateView):
    """材料登録ビュー."""

    model = Ingredient
    form_class = IngredientForm
    template_name = "ingredients/create.html"
    success_url = reverse_lazy("ingredients:list")

    def get_form_kwargs(self) -> dict[str, Any]:
        """フォームにユーザー情報を渡す."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """フォーム送信成功時の処理."""
        messages.success(self.request, f"材料「{form.cleaned_data['name']}」を登録しました。")
        return super().form_valid(form)


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    """材料編集ビュー."""

    model = Ingredient
    form_class = IngredientForm
    template_name = "ingredients/update.html"
    success_url = reverse_lazy("ingredients:list")

    def get_queryset(self) -> QuerySet[Ingredient]:
        """ログインユーザーの材料のみを取得."""
        return Ingredient.objects.filter(user=self.request.user)

    def get_form_kwargs(self) -> dict[str, Any]:
        """フォームにユーザー情報を渡す."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """フォーム送信成功時の処理."""
        messages.success(self.request, f"材料「{form.cleaned_data['name']}」を更新しました。")
        return super().form_valid(form)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    """材料削除ビュー."""

    model = Ingredient
    template_name = "ingredients/delete.html"
    success_url = reverse_lazy("ingredients:list")

    def get_queryset(self) -> QuerySet[Ingredient]:
        """ログインユーザーの材料のみを取得."""
        return Ingredient.objects.filter(user=self.request.user)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:  # noqa: ANN002, ANN003
        """削除実行時の処理."""
        ingredient = self.get_object()
        # get_objectの戻り値をIngredientとして扱う
        if isinstance(ingredient, Ingredient):
            ingredient_name = ingredient.name
            messages.success(request, f"材料「{ingredient_name}」を削除しました。")
        return super().delete(request, *args, **kwargs)
