from django.urls import path

from . import views

app_name = "ingredients"

urlpatterns = [
    # 材料一覧
    path("", views.IngredientListView.as_view(), name="list"),
    # 材料登録
    path("create/", views.IngredientCreateView.as_view(), name="create"),
    # 材料編集
    path("<int:pk>/update/", views.IngredientUpdateView.as_view(), name="update"),
    # 材料削除
    path("<int:pk>/delete/", views.IngredientDeleteView.as_view(), name="delete"),
]
