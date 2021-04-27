import datetime
import os
import random
from decimal import Decimal
from typing import cast

import api.settings as settings
import redis
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .tasks import find_first_user

redis_instance = redis.from_url(os.environ.get("REDIS_URL", ""), db=0)

# Class based views example

class HelloView(APIView):
  permission_classes = (IsAuthenticated,)

  def get(self, request):
    content = {'message': 'Hello, world!'}
    return Response(content)

class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `retrieve` actions.
  """

  queryset = User.objects.all()
  serializer_class = UserSerializer

  # override if you need to

  # def list(self, request, *args, **kwargs):
  #     return super().list(request, *args, **kwargs)

  # def update(self, request, *args, **kwargs):
  #     return super().update(request, *args, **kwargs)


# Regular views

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def check_auth(request):
  """
  Need to pass auth token for this endpoint to work.
  """
  # for json use:
  # return JsonResponse({'status': 'ok'})
  return HttpResponse('ok', status=status.HTTP_200_OK)


@api_view(['GET', 'OPTIONS'])
def check(request):
  return HttpResponse('ok', status=status.HTTP_200_OK)


@api_view(['GET', 'OPTIONS'])
# @permission_classes([IsAdminUser])
def index(request):
  context = {}
  return render(request, 'index.html', context)


# Example schedule a task on the backend
@api_view(['GET', 'OPTIONS'])
def trigger_celery_task(request):
  find_first_user.apply_async(('a byte!',))

  # other method
  find_first_user.delay('a byte!')

  # Schedule execution at 1AM next day
  now = datetime.datetime.utcnow()
  tomorrow = now + datetime.timedelta(1)
  late_night = tomorrow.replace(hour=1, minute=1)
  find_first_user.apply_async(('im a night owl',), eta=late_night)

  context = {'msg': 'task scheduled'}

  return render(request, 'index.html', context)

# Example interacting with redis
@api_view(['GET', 'OPTIONS'])
def push_to_redis_array(request):
  key = "TEST_REDIS"

  val = random.random()

  print(val, key)

  if val not in redis_instance.lrange(key, 0, -1):
    redis_instance.lpush(key, val)

  data = {'pushed': val, 'key': key}

  return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'OPTIONS'])
def remove_from_redis_array(request):

  key = "TEST_REDIS"
  l = redis_instance.lrange(key, 0, -1)

  val = l[0]
  redis_instance.lrem(key, 1, val)
  data = {'removed': val, 'key': key}

  return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'OPTIONS'])
def redis_list(request):

  key = "TEST_REDIS"
  l = redis_instance.lrange(key, 0, -1)
  data = {'values': l, 'key': key}

  return Response(data=data, status=status.HTTP_200_OK)
