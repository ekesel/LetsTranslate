from rest_framework import serializers
from .models import *

class inputSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=1000)
    text = serializers.CharField(max_length=100000)
