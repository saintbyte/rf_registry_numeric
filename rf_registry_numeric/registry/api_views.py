from django.db.models import Q
from registry.models import Registry
from registry.serializers import PhoneSerializer
from registry.serializers import RegistrySerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class FindPhoneView(APIView):
    """Поиск телефона в регистре"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        serializer = PhoneSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        code = phone[1:4]
        sub_phone = phone[4:]
        queryset = Registry.objects.filter(code=code)
        queryset_filter = Q()
        for i in range(len(sub_phone), 1, -1):
            sub_phone_slice = int(sub_phone[0:i])
            queryset_filter = queryset_filter | Q(
                start__lte=sub_phone_slice, end__gte=sub_phone_slice
            )
        queryset = queryset.filter(queryset_filter).order_by("-start", "-end")[0]
        if not queryset:
            return Response({"error": "Nothing found"})
        registy = RegistrySerializer(queryset).data
        return Response(
            {
                "phone": phone,
                "code": code,
                "registy": registy,
            }
        )
