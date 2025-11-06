from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pentru profil utilizator
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'nume', 'poza', 'rating',
                  'nr_antrenamente', 'grad', 'created_at', 'updated_at']
        read_only_fields = ['rating', 'nr_antrenamente', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pentru înregistrare utilizator nou
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    nume = serializers.CharField(required=True)
    grad = serializers.ChoiceField(choices=UserProfile.GRAD_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'nume', 'grad']

    def validate(self, data):
        """
        Verifică că parolele se potrivesc
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Parolele nu se potrivesc"})
        return data

    def create(self, validated_data):
        """
        Creează User și UserProfile
        """
        # Extrage datele pentru profil
        nume = validated_data.pop('nume')
        grad = validated_data.pop('grad')
        validated_data.pop('password_confirm')

        # Creează user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # Actualizează profilul creat automat de signal
        user.profile.nume = nume
        user.profile.grad = grad
        user.profile.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pentru User cu profil inclus
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
