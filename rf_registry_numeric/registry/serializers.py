from registry.models import Registry
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        min_length=11,
        max_length=25,
    )

    @staticmethod
    def normalize_phone(phone):
        phone = (
            phone.strip()
            .replace("-", "")
            .replace("+", "")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
        )
        if phone[0] == "8":
            phone = f"7{phone[1:]}"
        if phone[0] != "7":
            phone = f"7{phone}"
        return phone

    @staticmethod
    def validate_phone(phone):
        phone = PhoneSerializer.normalize_phone(phone)
        if len(phone) != 11:
            raise serializers.ValidationError("Invalid phone length")
        return phone


class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = "__all__"
