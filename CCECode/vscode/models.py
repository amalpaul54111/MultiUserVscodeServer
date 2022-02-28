from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Docker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    port = models.CharField(max_length=5)
    used = models.BooleanField(default=False)
    container = models.CharField(max_length=65,null=True, blank=True)
    
    def __str__(self):
        if(self.used):
            return f"{self.port} Used"
        else:
            return self.port