from django.db import models
from django.contrib.auth.models import User

class CloudImage(models.Model):
    image = models.ImageField()
    creation_date = models.DateTimeField('creation date')
    name = models.CharField(max_length=100, default='untitled')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
