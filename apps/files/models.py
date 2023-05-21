from django.db import models
from apps.base.models import BaseModel
from apps.modules.models import ModuleModel

import uuid

# Create your models here.

class FileModel(BaseModel):
    public_id = public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    module_id = models.ForeignKey(ModuleModel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/', max_length=100, null=True)


class CommentModel(BaseModel):
    public_id = public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    file_id = models.ForeignKey(FileModel, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=255)
    desc = models.CharField(max_length=50)