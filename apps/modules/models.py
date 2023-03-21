from django.db import models
from apps.base.models import BaseModel
from apps.folders.models import FolderModel

import uuid

# Create your models here.

class ModuleModel(BaseModel):
    public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    folder_id = models.ForeignKey(FolderModel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
