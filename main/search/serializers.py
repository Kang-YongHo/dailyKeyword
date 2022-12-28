from abc import ABC

from django.core import serializers
from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()

    class Meta:
        model = InputData
        fields = ('subject',)