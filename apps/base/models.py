from django.db import models

class BaseModel(models.Model):

    date_modified = models.DateField(auto_now=True)
    modified_by = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)