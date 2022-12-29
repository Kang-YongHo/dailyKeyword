import io

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import *
from .forms import *


def index(request):
    return render(request, 'search/index.html')


@api_view(['GET'])
def get_api(request):
    return None


@api_view(['POST'])
def post_api(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():

            result = find_keyword(serializer.validated_data['subject'])
            print(result)

            return Response(result, status=200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
