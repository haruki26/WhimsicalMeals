import json
import random
from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.generic import TemplateView

from dishes.models import GeneratedDish, Like

MIN_INGREDIENTS = 2


class CoreView(TemplateView):
    """トップページビュー."""

    template_name = "core/index.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # 最新料理を3つ取得
        recent_dishes = self.get_recent_dishes(limit=3)
        context["recent_dishes"] = recent_dishes

        # トップ3ランキングを取得
        top_dishes = self.get_top_dishes(limit=3)
        context["top_dishes"] = top_dishes

        # ユーザーのいいね情報を取得
        all_dishes = list(recent_dishes) + list(top_dishes)
        if self.request.user.is_authenticated:
            liked_dish_ids = Like.objects.filter(
                user=self.request.user,
                dish__in=all_dishes,
            ).values_list("dish_id", flat=True)
            context["user_liked_dish_ids"] = list(liked_dish_ids)
        else:
            context["user_liked_dish_ids"] = []

        return context

    def get_recent_dishes(self, limit: int | None = None) -> QuerySet[GeneratedDish]:
        """最新料理を取得するメソッド."""
        queryset = GeneratedDish.objects.order_by("-created_at").prefetch_related(
            "ingredients",
            "user",
        )
        if limit:
            return queryset[:limit]
        return queryset

    def get_top_dishes(self, limit: int | None = None) -> QuerySet[GeneratedDish]:
        """人気料理を取得するメソッド(いいね数順)."""
        queryset = GeneratedDish.objects.order_by(
            "-likes_count",
            "-created_at",
        ).prefetch_related(
            "ingredients",
            "user",
        )
        if limit:
            return queryset[:limit]
        return queryset


def demo_generate_dish(request: HttpRequest) -> JsonResponse:
    """デモ用の架空料理名生成API."""
    if request.method == "POST":
        data = json.loads(request.body)
        ingredients = data.get("ingredients", [])

        if len(ingredients) < MIN_INGREDIENTS:
            return JsonResponse(
                {
                    "error": "材料を2つ以上入力してください。",
                },
                status=400,
            )

        dish_name = generate_demo_dish_name(ingredients)

        return JsonResponse(
            {
                "dish_name": dish_name,
                "ingredients_used": ingredients,
            },
        )

    return JsonResponse({"error": "POSTメソッドのみ対応"}, status=405)


class DemoGenerateDishView(View):
    """デモ用の架空料理名生成API (クラスベース)."""

    def post(self, request: HttpRequest) -> JsonResponse:
        """POSTリクエストの処理."""
        try:
            data = json.loads(request.body)
            ingredients = data.get("ingredients", [])

            if len(ingredients) < MIN_INGREDIENTS:
                return JsonResponse(
                    {
                        "error": "材料を2つ以上入力してください。",
                    },
                    status=400,
                )

            dish_name = generate_demo_dish_name(ingredients)

            return JsonResponse(
                {
                    "dish_name": dish_name,
                    "ingredients_used": ingredients,
                },
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "無効なJSONデータです。",
                },
                status=400,
            )
        except (ValueError, KeyError):
            return JsonResponse(
                {
                    "error": "サーバーエラーが発生しました。",
                },
                status=500,
            )

    def get(self, _request: HttpRequest) -> JsonResponse:
        """GETリクエストの処理 (エラーレスポンス)."""
        return JsonResponse({"error": "POSTメソッドのみ対応"}, status=405)


def generate_demo_dish_name(ingredients: list[str]) -> str:
    """デモ用の料理名生成ロジック."""
    templates = [
        "{0}と{1}の{2}",
        "{0}入り{1}{2}",
        "秘伝の{0}{1}{2}",
        "{0}風{1}の{2}",
        "幻の{0}{1}{2}",
        "{0}香る{1}{2}",
        "謎の{0}{1}{2}",
        "伝説の{0}と{1}の{2}",
    ]

    suffixes = [
        "爆弾",
        "スープ",
        "炒め",
        "煮込み",
        "焼き",
        "蒸し",
        "サラダ",
        "パスタ",
        "カレー",
        "丼",
        "鍋",
        "グラタン",
        "フライ",
        "天ぷら",
        "寿司",
        "おにぎり",
        "闇鍋",
        "怪物",
        "伝説",
        "奇跡",
        "魔法",
        "究極",
        "至高",
        "禁断",
        "混沌",
        "神秘",
        "異次元",
        "宇宙",
    ]

    selected_ingredients = random.sample(ingredients, min(len(ingredients), 3))

    template = random.choice(templates)  # noqa: S311
    suffix = random.choice(suffixes)  # noqa: S311

    if len(selected_ingredients) >= MIN_INGREDIENTS:
        if "{2}" in template:
            dish_name = template.format(
                selected_ingredients[0],
                selected_ingredients[1],
                suffix,
            )
        else:
            dish_name = (
                template.format(
                    selected_ingredients[0],
                    selected_ingredients[1],
                )
                + suffix
            )
    else:
        dish_name = f"{selected_ingredients[0]}の{suffix}"

    return dish_name
