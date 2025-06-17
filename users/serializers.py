from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            role=validated_data.get('role', 'buyer')
        )
        return user



class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username')

    def create(self, validated_data):
        # Crée un utilisateur avec role admin et is_staff=True
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            role='admin',
            is_staff=True,
            is_superuser=False  # ou True si vous voulez superadmin
        )
        return user