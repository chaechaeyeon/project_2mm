from rest_framework import serializers
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
from posts import models

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
    class Meta:
        model = models.User
        fields = '__all__'
    def update(self, instance, validated_data):
        # 코드 값을 무시하고 업데이트할 필드만 validated_data에서 추출합니다.
        validated_data.pop('username', None)
        return super().update(instance, validated_data)

class UsersSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = models.UserInfo
        fields = '__all__'

    def update(self, instance, validated_data):
        # 전화번호 업데이트
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        #user = instance.user
        # 비밀번호 업데이트
        if 'password' in validated_data:
            new_password = validated_data['password']
            # user.set_password(new_password)
            # user.save()
            instance.user.set_password(new_password)
            instance.user.save()

        instance.save()
        return instance

# 모임코드생성 
class GroupSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = models.Group
        fields = ['name','info', 'profile', 'username', 'code']
    def update(self, instance, validated_data):
        # 코드 값을 무시하고 업데이트할 필드만 validated_data에서 추출합니다.
        validated_data.pop('code', None)
        return super().update(instance, validated_data)