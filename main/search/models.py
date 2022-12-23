
from django.db import models

# Create your models here.
class Search(models.Model):
    subject = models.CharField(max_length=100)
