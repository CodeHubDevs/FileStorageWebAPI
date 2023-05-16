from django.db import models
from apps.base.models import BaseModel
from apps.authentication.models import UserModel

import uuid

# Create your models here.

class ProfilePictureModel(BaseModel):
    public_id = public_id = models.UUIDField(default = uuid.uuid4,editable = False)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
    profile_picture = models.FileField(upload_to='files/', max_length=100, null=True)
    desc = models.CharField(max_length=50)
