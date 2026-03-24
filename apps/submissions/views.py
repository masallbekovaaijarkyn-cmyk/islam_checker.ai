from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Submission
from .serializers import (
    SubmissionCreateSerializer,
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionResultSerializer
)
from .filters import SubmissionFilter
from .choices import SubmissionStatus


class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionCreateSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Отправить задание на проверку",
        description="Создает новое задание и отправляет на проверку ИИ",
        request=SubmissionCreateSerializer,
        responses={201: SubmissionCreateSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubmissionListView(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SubmissionFilter
    search_fields = ['full_name', 'group_name', 'task_description', 'student_code']
    ordering_fields = ['created_at', 'score', 'full_name']
    ordering = ['-created_at']

    @extend_schema(
        summary="Получить список заданий",
        description="Возвращает список всех заданий с фильтрацией, поиском и сортировкой",
        parameters=[
            OpenApiParameter(name='search', description='Поиск по ФИО, группе, описанию', required=False, type=str),
            OpenApiParameter(name='group_name', description='Фильтр по названию группы', required=False, type=str),
            OpenApiParameter(name='task_type', description='Фильтр по типу задания (html, js, python, english)', required=False, type=str),
            OpenApiParameter(name='is_ai_generated', description='Фильтр по ИИ (true/false)', required=False, type=bool),
            OpenApiParameter(name='date_from', description='Дата с (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='date_to', description='Дата по (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='status', description='Статус проверки', required=False, type=str),
            OpenApiParameter(name='score_min', description='Минимальная оценка', required=False, type=int),
            OpenApiParameter(name='score_max', description='Максимальная оценка', required=False, type=int),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer
    lookup_field = 'id'

    @extend_schema(
        summary="Получить детальную информацию",
        description="Возвращает полную информацию о задании по ID",
        responses={200: SubmissionDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmissionResultView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionResultSerializer
    lookup_field = 'id'

    @extend_schema(
        summary="Получить результат проверки",
        description="Возвращает оценку и комментарий от ИИ",
        responses={200: SubmissionResultSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmissionCheckView(generics.GenericAPIView):
    queryset = Submission.objects.all()
    lookup_field = 'id'
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Запустить проверку",
        description="Запускает проверку задания с помощью ИИ",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        submission = self.get_object()
        submission.status = SubmissionStatus.PROCESSING
        submission.save()
        return Response({
            "message": "Проверка запущена",
            "submission_id": submission.id
        }, status=status.HTTP_200_OK)