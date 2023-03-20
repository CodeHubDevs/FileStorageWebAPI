from django.db import models
from apps.base.models import BaseModel
from apps.authentication.models import UserModel

import uuid

# Create your models here.

class FolderModel(BaseModel):
    
    public_id = public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
