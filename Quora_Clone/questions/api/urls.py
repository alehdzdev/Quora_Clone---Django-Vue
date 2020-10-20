from django.urls import include, path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from .views import AnswerCreateAPIView, AnswerLikeAPIView, AnswerRUDAPIView, QuestionAnswerListAPIView, QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("questions/<slug>/answers/", QuestionAnswerListAPIView.as_view(), name="answer-list"),
    path("questions/<slug>/answer/", AnswerCreateAPIView.as_view(), name="answer-create"),
    path("answers/<pk>/", AnswerRUDAPIView.as_view(), name="answer-detail"),
    path("answers/<pk>/like/", AnswerLikeAPIView.as_view(), name="answer-like"),
]