from django.db import models
from apps.base.models import BaseModel
from apps.folders.models import FolderModel

import uuid

# Create your models here.

class ChoiceModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    choice = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default="CHOICES")

class QuestionsModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    question = models.CharField(max_length=255)
    choices = models.ManyToManyField(ChoiceModel)
    type = models.CharField(max_length=50, default="QUESTIONS")

class QuizModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    folder_id = models.ForeignKey(FolderModel, on_delete=models.CASCADE, null=False)
    questions = models.ManyToManyField(QuestionsModel)
    type = models.CharField(max_length=50, default="QUIZ")