from rest_framework import serializers

from chats import models as chats_models, constants as chats_constants


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = chats_models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        """
        We override create method to encrypt the password which is done by set_password.First password is created by using super(DRF itself create it).
        """
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Similarly, update method is also override to encrypt the password in case when user updates the password.
        """
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = chats_models.Group
        fields = ['id', 'title']

    def create(self, validated_data):
        """
        We override this create method, to add the user in the group when group created and make the same user as admin.
        """
        group = super().create(validated_data)
        user = self.context["request"].user
        chats_models.UserGroup.objects.create(
            group=group, user=user, role=chats_constants.ADMIN)
        return group


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = chats_models.UserGroup
        fields = ['id', 'group', 'user', 'role']
    
    def validate(self, data):
        """
        This validation is applied to assure that only admin of the group is making other user admin.
        """
        user = self.context["request"].user
        if 'role' in data and data['role'] == chats_constants.ADMIN and user.role != chats_constants.chats_constants.ADMIN:
            raise serializers.ValidationError(chats_constants.ONLY_ADMIN_CAN_CHANGE_THE_ROLE)
        
        return data
