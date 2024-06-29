from rest_framework import serializers
from .models import *

class WastePickRequestSerializer(serializers.Serializer):
    type_of_waste = serializers.CharField()
