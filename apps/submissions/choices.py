from django.db import models

class TaskType(models.TextChoices):
    HTML = 'html', 'HTML/CSS'
    JS = 'js', 'JavaScript'
    PYTHON = 'python', 'Python'
    ENGLISH = 'english', 'English'

class SubmissionStatus(models.TextChoices):
    PENDING = 'pending', 'В ожидании'
    PROCESSING = 'processing', 'Проверяется'
    COMPLETED = 'completed', 'Проверено'
    ERROR = 'error', 'Ошибка'
