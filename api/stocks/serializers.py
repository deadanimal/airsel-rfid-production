from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now

from .models import (
    Stock,
    Receive,
    Issuance,
    Return,
    Purchase,
    Dispose,
    Reversal,
    Transfer,
    Count
)

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'


class ReceiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receive
        fields = '__all__'


class IssuanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issuance
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Return
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = '__all__'


class DisposeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dispose
        fields = '__all__'


class ReversalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reversal
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = '__all__'


class CountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Count
        fields = '__all__'