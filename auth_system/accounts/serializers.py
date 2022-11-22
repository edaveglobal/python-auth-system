from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class GathpayUserAccountRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'is_superuser',
            'is_active',
            'date_joined')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password and Password2 didn't match."})

        return attrs

    def create(self, validated_data):
            
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize()
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class GathpayUsersAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'date_joined')


class UpdateUserAccountPasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(write_only=True, required=True)

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])

    class Meta:
        model = User
        fields = ('new_password', 'old_password')

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        attrs = super().validate(attrs)
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'non_field_errors': ['Old password and new passwords can\'t be the same.']
            })

        if not self.instance.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                'old_password': ['Password is incorrect.']
            })

        return attrs

    def update(self, instance, validated_data: Dict[str, Any]) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
