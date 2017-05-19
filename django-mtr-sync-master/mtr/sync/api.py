from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import Settings, Field


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field


class SettingsAPI(
        generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class FieldAPI(
        generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Field.objects.all()
    serializer_class = FieldSerializer
