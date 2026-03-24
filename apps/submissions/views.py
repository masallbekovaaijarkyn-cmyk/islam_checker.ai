from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


class SubmissionListView(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubmissionFilter
    search_fields = ['full_name', 'group_name', 'task_description', 'student_code']
    ordering_fields = ['created_at', 'score', 'full_name']
    ordering = ['-created_at']


class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer
    lookup_field = 'id'


class SubmissionResultView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionResultSerializer
    lookup_field = 'id'


class SubmissionCheckView(generics.GenericAPIView):
    queryset = Submission.objects.all()
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        submission = self.get_object()
        submission.status = SubmissionStatus.PROCESSING
        submission.save()
        return Response({
            "message": "Проверка запущена",
            "submission_id": submission.id
        }, status=status.HTTP_200_OK)
