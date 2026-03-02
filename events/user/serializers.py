from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'role', 
            'college', 'branch', 'year',
            'organization_name', 'is_verified_organizer',
            'profile_picture', 'bio',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_verified_organizer']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'role', 'college', 'branch', 'year', 'organization_name'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # If role is student, require college info
        if data['role'] == 'student':
            if not data.get('college') or not data.get('branch'):
                raise serializers.ValidationError("Students must provide college and branch")
        
        # If role is organizer, require organization name
        if data['role'] == 'organizer':
            if not data.get('organization_name'):
                raise serializers.ValidationError("Organizers must provide organization name")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)