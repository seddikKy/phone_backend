from rest_framework import serializers

from core.models import Tier, Contact, Role, CallLog, NewUser, Position


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ['tier_name', 'address', 'email', 'created_at', 'is_active']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact_name', 'phone_number', 'id_role', 'created_at', 'id_tier', 'id_user']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_name']


class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['id', 'id_user', 'call_type', 'id_call', 'call_started_at', 'duration', 'id_log',
                  'called_phone_number', 'position_call_log', 'id_device', 'reception_date']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'id_device', 'max_position_call_log', 'reception_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id', 'email', 'user_name', 'first_name', 'about', 'is_active', 'is_staff']

        extra_kwarg = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
