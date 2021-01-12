from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class File(models.Model):
    filename = models.CharField(null=True, max_length=50)
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    date_uploaded = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.filename
