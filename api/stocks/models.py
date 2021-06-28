# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from simple_history.models import HistoricalRecords

from users.models import (
    CustomUser
)
from organisations.models import (
    Organisation
)

from core.helpers import PathAndRename

class Stock(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    short_description = models.CharField(max_length=100, default='NA')
    long_description = models.TextField(default='NA')
    total_quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Receive(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    received_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='receive_receive_by')
    received_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.received_at)


class Issuance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='issuance_stock')
    quantity = models.IntegerField(default=1)
    issuanced_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='issuance_issuanced_by')
    issuanced_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.issuanced_at)


class Return(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='return_stock')
    quantity = models.IntegerField(default=1)
    returned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='return_returned_by')
    returned_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.returned_at)


class Purchase(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.CharField(max_length=100, default='NA')
    delivery_order = models.CharField(max_length=100, default='NA')

    supplier = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='purchase_supplier')
    stock_receive  = models.ForeignKey(Receive, on_delete=models.CASCADE, null=True, related_name='purchase_stock_receive')
    stock_return = models.ForeignKey(Return, on_delete=models.CASCADE, null=True, related_name='purchase_stock_return')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.purchase_order, self.delivery_order)


class Dispose(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='dispose_stock')
    quantity = models.IntegerField(default=1)
    disposed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='dispose_disposed_by')
    disposed_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.disposed_at)


class Reversal(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='reversal_stock')
    quantity = models.IntegerField(default=1)
    reversal_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='reversal_reversal_by')
    reversal_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.reversal_at)


class Transfer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='transfer_stock')
    quantity = models.IntegerField(default=1)
    transfered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='transfer_transfered_by')
    transfered_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.transfered_at)


class Count(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name='count_stock')
    quantity = models.IntegerField(default=1)
    counted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='count_counted_by')
    counted_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return "{} {}".format(self.stock, self.counted_at)