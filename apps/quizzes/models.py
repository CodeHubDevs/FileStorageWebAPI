from django.db import models
from apps.base.models import BaseModel
from apps.folders.models import FolderModel

import uuid

# Create your models here.

class QuizQuestionsModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    folder_id = models.ForeignKey(FolderModel, on_delete=models.CASCADE, null=False)
    question = models.CharField(max_length=255)
    desc = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="QUIZ")

class QuizChoicesModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    question_id = models.ForeignKey(QuizQuestionsModel, on_delete=models.CASCADE, null=False)
    answer = models.CharField(max_length=255)
    desc = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="QUIZ")