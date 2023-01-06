from abc import ABC

from django.core import serializers
from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()

    class Meta:
        model = InputData
        fields = ('year', 'month', 'subject')
