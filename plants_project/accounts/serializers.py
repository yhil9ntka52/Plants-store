from django.contrib.auth.models import User
from rest_framework import serializers
import re

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate_email(self, value):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate(self, data):
        errors = []
        if not data.get('username'):
            errors.append("Username is required")
        if not data.get('email'):
            errors.append("Email is required")
        if not data.get('password') or not data.get('password2'):
            errors.append("Password is required")
        if errors:
            raise serializers.ValidationError(errors)
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password is too short")
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
