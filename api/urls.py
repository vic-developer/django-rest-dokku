"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

from api.core import views

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    # 'post': 'create'
})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    url('auth/', include('dj_rest_auth.urls')),
    url('registration/', include('dj_rest_auth.registration.urls')),

    # Api
    url('api/check/secured', views.check_auth),
    url('api/check', views.check),
    url('api/index', views.index),
    url('api/test_task', views.trigger_celery_task),
    url('redis/push', views.push_to_redis_array),
    url('redis/remove', views.remove_from_redis_array),
    url('redis/list', views.redis_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
