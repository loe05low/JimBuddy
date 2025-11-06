from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BlockedUser


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pentru profil utilizator
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'nume', 'avatar', 'avatar_url', 'bio',
                  'city', 'phone', 'rating', 'nr_antrenamente', 'grad', 'current_streak',
                  'last_workout_date', 'created_at', 'updated_at']
        read_only_fields = ['rating', 'nr_antrenamente', 'current_streak', 'last_workout_date',
                           'created_at', 'updated_at']

    def get_avatar_url(self, obj):
        """
        Returnează URL-ul complet al avatar-ului
        """
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


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


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pentru editarea profilului utilizator
    """
    class Meta:
        model = UserProfile
        fields = ['nume', 'avatar', 'bio', 'city', 'phone', 'grad']

    def validate_bio(self, value):
        """
        Validează că bio-ul nu depășește 140 caractere
        """
        if value and len(value) > 140:
            raise serializers.ValidationError("Bio-ul nu poate depăși 140 de caractere")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pentru User cu profil inclus
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class BlockedUserSerializer(serializers.ModelSerializer):
    """
    Serializer pentru utilizatori blocați
    """
    blocker_details = UserProfileSerializer(source='blocker', read_only=True)
    blocked_details = UserProfileSerializer(source='blocked', read_only=True)

    class Meta:
        model = BlockedUser
        fields = ['id', 'blocker', 'blocker_details', 'blocked', 'blocked_details', 'reason', 'created_at']
        read_only_fields = ['id', 'blocker', 'created_at']
