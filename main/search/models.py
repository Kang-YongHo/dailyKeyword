import peewee
from peewee import *
from django.db import models

db = MySQLDatabase('test', user='root', passwd='1234')

class BaseModel(Model):
    class Meta:
        database = db
class Keyword(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.id)

class Analysis(models.Model):
    date = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    expect = models.CharField(max_length=20)

class InputData(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    subject = models.CharField(max_length=20)



