import io

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .forms import *
from .serializers import *


def index(request):
    return render(request, 'search/index.html')


@api_view(['GET'])
def get_api(request):
    return None


@api_view(['POST'])
def search(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)
    serializer = SubjectSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    result = find_keyword(serializer.validated_data['subject'],
                          serializer.validated_data['year'],
                          serializer.validated_data['month'])
    print(result)

    return Response(result, status=200)


@api_view(['GET'])
def update_db(request):
    db_update()
    return HttpResponse(status=200)
