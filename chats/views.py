from rest_framework import permissions, viewsets

from chats import models as chats_models, serializers as account_serializers, permissions as chats_custom_permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset handles all the CRUD operations on USER.
    We have set Token authentication by default in settings, so here define different permissions for different actions.User can retrieve only his own details.
    """
    serializer_class = account_serializers.UserSerializer

    def get_queryset(self):
        return chats_models.User.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, chats_custom_permissions.IsOwner]
        return [permission() for permission in permission_classes]


class GroupViewset(viewsets.ModelViewSet):
    "This Viewset handles all the CRUD operations on Group, like create any group, update title of group, delete the group or retrieve the group"
    queryset = chats_models.Group.objects.all()
    serializer_class = account_serializers.GroupSerializer


class UserGroupViewSet(viewsets.ModelViewSet):
    """
    This viewsets handles all the CRUD operations related to user and group, like add or remove any user from any group, make any user admin of the group.User can only access/retrieve the groups with which he is related.
    """
    serializer_class = account_serializers.UserGroupSerializer

    def get_queryset(self):
         return chats_models.UserGroup.objects.filter(user=self.request.user)
