"""料理生成アプリのURL設定."""

from django.urls import path

from . import views

app_name = "dishes"

urlpatterns = [
    path("", views.DishListView.as_view(), name="list"),
    path("generate/", views.DishGenerateView.as_view(), name="generate"),
    path("save/", views.SaveDishView.as_view(), name="save"),
    path("ranking/", views.RankingListView.as_view(), name="ranking"),
    path("recent/", views.RecentDishesView.as_view(), name="recent"),
    path("like/<int:dish_id>/", views.ToggleLikeView.as_view(), name="toggle_like"),
    path("delete/<int:dish_id>/", views.DishDeleteView.as_view(), name="delete"),
    path("demo/", views.DemoGenerateView.as_view(), name="demo"),
]
