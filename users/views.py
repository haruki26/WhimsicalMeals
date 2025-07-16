from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class LoginView(TemplateView):
    """ログインビュー."""

    template_name = "users/login.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = AuthenticationForm()
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"ようこそ、{username}さん!")
                return redirect("index")
            messages.error(request, "ユーザー名またはパスワードが間違っています。")

        return render(request, self.template_name, {"form": form})


class LogoutView(TemplateView):
    """ログアウトビュー."""

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        messages.success(request, "ログアウトしました。")
        return redirect("index")


class SignUpView(CreateView):
    """ユーザー登録ビュー."""

    form_class = UserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, "アカウントが作成されました。ログインしてください。")
        return response
