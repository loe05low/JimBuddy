from rest_framework import serializers
from .models import Rating
from users.serializers import UserProfileSerializer


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer pentru rating-uri și comentarii
    Include detalii despre utilizatori
    """
    from_user_details = UserProfileSerializer(source='from_user', read_only=True)
    to_user_details = UserProfileSerializer(source='to_user', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'from_user', 'from_user_details', 'to_user', 'to_user_details',
                  'sesiune', 'rating', 'feedback', 'comentariu', 'data']
        read_only_fields = ['id', 'from_user', 'data']

    def validate_rating(self, value):
        """
        Validează că rating-ul este între 1 și 5
        """
        if value < 1.0 or value > 5.0:
            raise serializers.ValidationError("Rating-ul trebuie să fie între 1 și 5")
        return value

    def validate(self, data):
        """
        Setează from_user ca user-ul curent
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['from_user'] = request.user.profile
        return data


class RatingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer simplificat pentru creare rating
    """
    class Meta:
        model = Rating
        fields = ['to_user', 'sesiune', 'rating', 'feedback', 'comentariu']

    def validate_rating(self, value):
        """
        Validează că rating-ul este între 1 și 5
        """
        if value < 1.0 or value > 5.0:
            raise serializers.ValidationError("Rating-ul trebuie să fie între 1 și 5")
        return value

    def validate_feedback(self, value):
        """
        Validează că feedback-ul nu depășește 50 caractere
        """
        if value and len(value) > 50:
            raise serializers.ValidationError("Feedback-ul nu poate depăși 50 de caractere")
        return value
