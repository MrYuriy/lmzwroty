from rest_framework import serializers
from .models import Adres
class GenadresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adres
        fields = ['adreses']