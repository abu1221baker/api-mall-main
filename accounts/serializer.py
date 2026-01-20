from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Profile(**validated_data)
        user.set_password(password)  # ✅ hashes password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password hashing on update
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance