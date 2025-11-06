from rest_framework import serializers
from .models import Sesiune, Cerere
from users.serializers import UserProfileSerializer
from gyms.serializers import SalaSerializer


class SesiuneSerializer(serializers.ModelSerializer):
    """
    Serializer pentru sesiuni de antrenament
    Include detalii despre user și sală
    """
    user_details = UserProfileSerializer(source='user', read_only=True)
    sala_details = SalaSerializer(source='sala', read_only=True)

    class Meta:
        model = Sesiune
        fields = ['id', 'user', 'user_details', 'sala', 'sala_details',
                  'tip_antrenament', 'interval_orar', 'descriere', 'status',
                  'data_creare', 'data_expirare']
        read_only_fields = ['id', 'data_creare', 'status']

    def validate(self, data):
        """
        Setează user-ul curent ca owner al sesiunii
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['user'] = request.user.profile
        return data


class SesiuneCreateSerializer(serializers.ModelSerializer):
    """
    Serializer simplificat pentru creare sesiune
    """
    class Meta:
        model = Sesiune
        fields = ['sala', 'tip_antrenament', 'interval_orar', 'descriere', 'data_expirare']


class CerereSerializer(serializers.ModelSerializer):
    """
    Serializer pentru cereri de gym buddy
    Include detalii despre applicant și sesiune
    """
    applicant_details = UserProfileSerializer(source='applicant', read_only=True)
    sesiune_details = SesiuneSerializer(source='sesiune', read_only=True)

    class Meta:
        model = Cerere
        fields = ['id', 'sesiune', 'sesiune_details', 'applicant', 'applicant_details',
                  'status', 'data_creare', 'data_raspuns']
        read_only_fields = ['id', 'applicant', 'status', 'data_creare', 'data_raspuns']

    def validate(self, data):
        """
        Setează applicant-ul ca user-ul curent
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['applicant'] = request.user.profile
        return data


class CerereUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pentru acceptare/refuzare cerere
    """
    class Meta:
        model = Cerere
        fields = ['status']

    def validate_status(self, value):
        """
        Validează că status-ul este acceptat sau refuzat
        """
        if value not in ['acceptat', 'refuzat']:
            raise serializers.ValidationError("Status trebuie să fie 'acceptat' sau 'refuzat'")
        return value
