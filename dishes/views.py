"""料理生成関連のビュー."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView,
    View,
)

from ingredients.models import Ingredient

from .forms import DishGenerationForm
from .models import GeneratedDish, Like
from .utils import generate_multiple_dish_names


class DishListView(LoginRequiredMixin, ListView):
    """自分が保存した料理一覧ビュー."""

    model = GeneratedDish
    template_name = "dishes/list.html"
    context_object_name = "dishes"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[GeneratedDish]:
        """ログインユーザーの料理のみ取得."""
        return GeneratedDish.objects.filter(user=self.request.user).prefetch_related(
            "ingredients",
        )


class RankingListView(ListView):
    """料理ランキングビュー(ログイン不要)."""

    model = GeneratedDish
    template_name = "dishes/ranking.html"
    context_object_name = "dishes"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[GeneratedDish]:
        """いいね数順で料理を取得."""
        return GeneratedDish.objects.order_by(
            "-likes_count",
            "-created_at",
        ).prefetch_related(
            "ingredients",
            "user",
        )

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """コンテキストデータを追加."""
        context = super().get_context_data(**kwargs)

        # ユーザーのいいね情報を取得
        if self.request.user.is_authenticated:
            dishes = context["dishes"]
            liked_dish_ids = Like.objects.filter(
                user=self.request.user,
                dish__in=dishes,
            ).values_list("dish_id", flat=True)
            context["user_liked_dish_ids"] = list(liked_dish_ids)
        else:
            context["user_liked_dish_ids"] = []

        return context


class DishGenerateView(LoginRequiredMixin, View):
    """料理名生成ビュー."""

    template_name = "dishes/generate.html"
    form_class = DishGenerationForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """GETリクエストの処理."""
        form = self.form_class()
        user_ingredients = Ingredient.objects.filter(user=request.user)
        context = {
            "form": form,
            "user_ingredients": user_ingredients,
            "ingredients_count": user_ingredients.count(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """POSTリクエストの処理."""
        form = self.form_class(request.POST)
        if form.is_valid():
            # ユーザーの材料を取得
            user_ingredients = list(
                Ingredient.objects.filter(user=request.user),
            )

            if len(user_ingredients) < 2:  # noqa: PLR2004
                messages.error(
                    request,
                    "料理を生成するには少なくとも2つの材料を登録してください。",
                )
                return redirect("ingredients:list")

            try:
                # 材料名のリストを作成
                ingredient_names = [ing.name for ing in user_ingredients]
                # 複数の料理名を生成
                dish_names = generate_multiple_dish_names(ingredient_names, count=3)
                context = {
                    "form": form,
                    "generated_dishes": dish_names,
                    "user_ingredients": user_ingredients,
                }
                return render(request, self.template_name, context)
            except ValueError as e:
                messages.error(request, str(e))
                return redirect("dishes:generate")

        # フォームが無効な場合
        user_ingredients = Ingredient.objects.filter(user=request.user)
        context = {
            "form": form,
            "user_ingredients": user_ingredients,
            "ingredients_count": user_ingredients.count(),
        }
        return render(request, self.template_name, context)


class SaveDishView(LoginRequiredMixin, View):
    """生成された料理を保存するビュー."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """POSTリクエストの処理."""
        dish_name = request.POST.get("dish_name")
        ingredient_ids = request.POST.getlist("ingredient_ids")

        if not dish_name:
            messages.error(request, "料理名が指定されていません。")
            return redirect("dishes:generate")

        # 材料を取得, ユーザーの材料のみ
        ingredients = Ingredient.objects.filter(
            id__in=ingredient_ids,
            user=request.user,
        )

        if not ingredients.exists():
            messages.error(request, "有効な材料が選択されていません。")
            return redirect("dishes:generate")

        # 料理を保存
        dish = GeneratedDish.objects.create(
            name=dish_name,
            user=request.user,
        )
        dish.ingredients.set(ingredients)

        messages.success(request, f"「{dish_name}」を保存しました!")
        return redirect("dishes:list")


class ToggleLikeView(LoginRequiredMixin, View):
    """いいねのトグルビュー."""

    def post(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """POSTリクエストの処理."""
        dish = get_object_or_404(GeneratedDish, id=dish_id)

        # 自分の料理にはいいねできない
        if dish.user == request.user:
            messages.error(request, "自分の料理にはいいねできません。")
            return redirect("dishes:ranking")

        like, created = Like.objects.get_or_create(
            dish=dish,
            user=request.user,
        )

        if not created:
            # 既にいいねしていた場合は削除
            like.delete()
            messages.info(request, f"「{dish.name}」のいいねを取り消しました。")
        else:
            messages.success(request, f"「{dish.name}」にいいねしました!")

        # リファラーまたはランキングページにリダイレクト
        return redirect(request.META.get("HTTP_REFERER", "dishes:ranking"))


class DishDeleteView(LoginRequiredMixin, View):
    """料理の削除ビュー."""

    template_name = "dishes/delete.html"

    def get(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """GETリクエストの処理."""
        dish = get_object_or_404(GeneratedDish, id=dish_id, user=request.user)
        return render(request, self.template_name, {"dish": dish})

    def post(self, request: HttpRequest, dish_id: int) -> HttpResponse:
        """POSTリクエストの処理."""
        dish = get_object_or_404(GeneratedDish, id=dish_id, user=request.user)
        dish_name = dish.name
        dish.delete()
        messages.success(request, f"「{dish_name}」を削除しました。")
        return redirect("dishes:list")


class DemoGenerateView(View):
    """デモ用料理生成ビュー(ログイン不要)."""

    template_name = "dishes/demo.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """GETリクエストの処理."""
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        """POSTリクエストの処理."""
        # POSTデータから材料名を取得
        ingredient_names = [name.strip() for name in request.POST.get("ingredients", "").split(",") if name.strip()]

        if len(ingredient_names) < 2:  # noqa: PLR2004
            messages.error(request, "少なくとも2つの材料を入力してください。")
            return render(request, self.template_name)

        try:
            dish_names = generate_multiple_dish_names(ingredient_names, count=3)
            context = {
                "generated_dishes": dish_names,
                "input_ingredients": ingredient_names,
                "is_demo": True,
            }
            return render(request, self.template_name, context)
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, self.template_name)

        return render(request, self.template_name)


class RecentDishesView(ListView):
    """最新の料理表示ビュー(ログイン不要)."""

    model = GeneratedDish
    template_name = "dishes/recent.html"
    context_object_name = "dishes"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[GeneratedDish]:
        """最新の料理を取得."""
        return GeneratedDish.objects.order_by(
            "-created_at",
        ).prefetch_related("ingredients", "user")

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """ユーザーのいいね情報を追加."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_dish_ids = Like.objects.filter(
                user=self.request.user,
                dish__in=context["dishes"],
            ).values_list("dish_id", flat=True)
            context["user_liked_dish_ids"] = list(liked_dish_ids)
        else:
            context["user_liked_dish_ids"] = []
        return context
