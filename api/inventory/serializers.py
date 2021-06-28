from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now

from .models import (
    InventoryItem,
    # InventoryItemUomIntra,
    # InventoryItemUomInter,
    InventoryPurchaseOrder,
    InventoryGrn,
    InventoryTransaction,
    InventoryMaterial
)

from users.serializers import (
    CustomUserSerializer
)

class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = '__all__'

# class InventoryItemUomIntraSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = InventoryItemUomIntra
#         fields = '__all__'

# class InventoryItemUomInterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = InventoryItemUomInter
#         fields = '__all__'

class InventoryPurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryPurchaseOrder
        fields = '__all__'

class InventoryGrnSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryGrn
        fields = '__all__'

class InventoryTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryTransaction
        fields = '__all__'

class InventoryMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryMaterial
        fields = '__all__'