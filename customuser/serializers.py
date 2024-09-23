from rest_framework import serializers
from .models import CustomUser
from datetime import date

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined', 'is_active']
        extra_kwargs = {
            'username': {'required': True},
            'birth_date': {'required': True},
            'password': {'required': True}
        }

    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("User must be at least 15 years old.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
