from django.db import router
from django.urls import include, path
from rest_framework import routers

from chats import views as chats_views


router = routers.DefaultRouter()
router.register(r'users', chats_views.UserViewSet, basename="user")
router.register(r'groups', chats_views.GroupViewset, basename="group")
router.register(r'user-group', chats_views.UserGroupViewSet, basename="user-group")

urlpatterns = [
    path('', include(router.urls)),
]
