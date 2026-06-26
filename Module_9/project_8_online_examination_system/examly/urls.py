# ============================================================================
#  urls.py — frontend + API router + auth + Swagger + admin.
# ============================================================================
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from exams.api_views import (
    ExamViewSet, QuestionViewSet, ChoiceViewSet, AttemptViewSet,
)

router = DefaultRouter()
router.register("exams", ExamViewSet)
router.register("questions", QuestionViewSet)
router.register("choices", ChoiceViewSet)
router.register("attempts", AttemptViewSet, basename="attempt")

urlpatterns = [
    path("", TemplateView.as_view(template_name="exam.html"), name="home"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/login/", obtain_auth_token, name="api-login"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
