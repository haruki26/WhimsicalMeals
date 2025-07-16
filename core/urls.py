from django.urls import path

from core.views import CoreView, DemoGenerateDishView, demo_generate_dish

urlpatterns = [
    path("", CoreView.as_view(), name="index"),
    path("api/demo/generate-dish/", DemoGenerateDishView.as_view(), name="demo_generate_dish_class"),
    # 後方互換性のため関数ベースも残す
    path("api/demo/generate-dish-func/", demo_generate_dish, name="demo_generate_dish"),
]
