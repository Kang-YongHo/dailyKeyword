from django.core import serializers
from rest_framework import serializers
from .models import Search

class SubjectSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=100)
