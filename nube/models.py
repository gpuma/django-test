from django.db import models

class CloudImage(models.Model):
    image = models.ImageField()
    pub_date = models.DateTimeField()
    name = models.CharField(max_length=50, default='untitled')
