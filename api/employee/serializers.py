from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now

from .models import (
    Employee,
    FailureProfile,
    ApprovalProfile,
    ContactInformation
)

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

class FailureProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailureProfile
        fields = '__all__'

class ApprovalProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalProfile
        fields = '__all__'

class ContactInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactInformation
        fields = '__all__'