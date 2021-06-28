from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now

from .models import (
    Store,
    Region,
    Location,
    State
)

from users.serializers import (
    CustomUserSerializer
)

class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class StoreExtendedSerializer(serializers.ModelSerializer):
    supervisor = CustomUserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = '__all__'


class LocationExtendedSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Location
        fields = '__all__'
    

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'
