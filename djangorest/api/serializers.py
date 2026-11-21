from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, trim_whitespace=True)

    class Meta:
        model = User
        fields = ["id", "name", "age"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        if not any(ch.isalpha() for ch in value):
            raise serializers.ValidationError("Name must contain at least one letter.")
        return value
