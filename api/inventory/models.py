from __future__ import unicode_literals
import uuid

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from simple_history.models import HistoricalRecords

from users.models import (
    CustomUser
)

from core.helpers import PathAndRename

class InventoryItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record_type = models.IntegerField(blank=True, default='0')
    item_number = models.CharField(max_length=300, default='',blank=True)
    inventory_org_code = models.CharField(max_length=18, default='',blank=True)
    legal_entity_code = models.CharField(max_length=120, default='',blank=True)
    legal_entity_me = models.CharField(max_length=960, default='',blank=True)
    short_description = models.CharField(max_length=240, default='',blank=True)
    long_description = models.CharField(max_length=2000, default='',blank=True)
    primary_uom = models.CharField(max_length=12, default='',blank=True)
    secondary_uom = models.CharField(max_length=12, default='',blank=True)
    item_status = models.CharField(max_length=10, default='',blank=True)
    item_category = models.CharField(max_length=1000, default='',blank=True)
    inventory_item = models.CharField(max_length=1, default='',blank=True)
    transfer_orders_enbled = models.CharField(max_length=1, default='',blank=True)
    purchasable_item = models.CharField(max_length=1, default='',blank=True)
    shippable_item = models.CharField(max_length=1, default='',blank=True)

    # class meta:
    #     ordering = ['name']
    
    # def __str__(self):
    #     return self.name
    
# class InventoryItemUomIntra(models.Model):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     record_type = models.IntegerField(blank=True, default='0')
#     item_number = models.CharField(max_length=300, default='',blank=True)
#     from_uom_code = models.CharField(max_length=100, default='',blank=True)
#     uom_class = models.CharField(max_length=40, default='',blank=True)
#     conversion_rate = models.CharField(max_length=22, default='',blank=True)
#     base_uom_rate = models.CharField(max_length=100, default='',blank=True)
#     end_date = models.DateTimeField(auto_now=True)
#     attribute1 = models.CharField(max_length=18, default='',blank=True)

#     # class meta:
#     #     ordering = ['name']
    
#     # def __str__(self):
#     #     return self.name

# class InventoryItemUomInter(models.Model):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     record_type = models.IntegerField(blank=True, default='0')
#     item_number = models.CharField(max_length=300, default='',blank=True)
#     from_base_uom_code = models.CharField(max_length=100, default='',blank=True)
#     from_uom_class = models.CharField(max_length=100, default='',blank=True)
#     conversion_rate = models.CharField(max_length=22, default='',blank=True)
#     to_base_uom_code = models.CharField(max_length=100, default='',blank=True)
#     to_uom_class = models.CharField(max_length=40, default='',blank=True)
#     end_date = models.DateTimeField(auto_now=True)
#     attribure1 = models.CharField(max_length=18, default='',blank=True)

# #     # class meta:
# #     #     ordering = ['name']
    
# #     # def __str__(self):
# #     #     return self.name

class InventoryPurchaseOrder(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_number = models.CharField(max_length=30, default='0')
    change_order_number = models.CharField(max_length=100, default='',blank=True)
    change_order_status = models.CharField(max_length=100, default='',blank=True)
    description = models.CharField(max_length=240, default='',blank=True)
    procurement_bu = models.CharField(max_length=960, default='',blank=True)
    sold_to_legal_entity = models.CharField(max_length=240, default='',blank=True)
    buyer = models.CharField(max_length=2000, default='',blank=True)
    supplier_number = models.CharField(max_length=30, default='',blank=True)
    supplier_site_code = models.CharField(max_length=15, default='',blank=True)
    
    address_name = models.CharField(max_length=240, default='',blank=True)
    address_line_1 = models.CharField(max_length=240, default='',blank=True)
    address_line_2 = models.CharField(max_length=240, default='',blank=True)
    address_line_3 = models.CharField(max_length=240, default='',blank=True)
    city = models.CharField(max_length=60, default='',blank=True)
    state = models.CharField(max_length=60, default='',blank=True)
    postal_code = models.CharField(max_length=20, default='',blank=True)
    country = models.CharField(max_length=60, default='',blank=True)

    contact_first_name = models.CharField(max_length=150, default='',blank=True)
    contact_last_name = models.CharField(max_length=150, default='',blank=True)
    contact_email_address = models.CharField(max_length=2000, default='',blank=True)
    contact_mobile_number = models.CharField(max_length=60, default='',blank=True)
    contact_phone_number = models.CharField(max_length=60, default='',blank=True)
    supplier_contact = models.CharField(max_length=360, default='',blank=True)

    line_num = models.IntegerField(blank=True, default='0')
    schedule_num = models.IntegerField(blank=True, default='0')
    distribution_num = models.IntegerField(blank=True, default='0')
    item_number = models.CharField(max_length=300, default='',blank=True)

    line_description = models.CharField(max_length=240, default='',blank=True)
    quantity = models.IntegerField(blank=True, default='0')
    uom_code = models.CharField(max_length=25, default='',blank=True)
    base_quantity = models.IntegerField(blank=True, default='0')
    base_uom_code = models.CharField(max_length=25, default='',blank=True)
    requested_date = models.DateTimeField(auto_now=True)
    ship_to_organization = models.CharField(max_length=18, default='',blank=True)
    sub_inventory_code = models.CharField(max_length=10, default='',blank=True)
    ship_to_location = models.CharField(max_length=60, default='',blank=True)
    line_type = models.CharField(max_length=30, default='',blank=True)
    line_status = models.CharField(max_length=100, default='',blank=True)

#     # class meta:
#     #     ordering = ['name']
    
#     # def __str__(self):
#     #     return self.name

class InventoryGrn(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    header_interface_number = models.CharField(max_length=100,blank=True, default='0')
    receipt_source_code = models.CharField(max_length=10, default='',blank=True)
    business_unit = models.CharField(max_length=240, default='',blank=True)
    business_type = models.CharField(max_length=240, default='',blank=True)
    # transaction_type = models.CharField(max_length=25, default='',blank=True)
    receipt_number = models.CharField(max_length=30, default='',blank=True)
    supplier_number = models.CharField(max_length=20, default='',blank=True)
    supplier_site_code = models.CharField(max_length=35, default='',blank=True)
    bill_of_lading = models.CharField(max_length=25, default='',blank=True)
    packing_slip = models.CharField(max_length=25, default='',blank=True)
    carrier_name = models.CharField(max_length=50, default='',blank=True)
    way_bill = models.CharField(max_length=20, default='',blank=True)
    comments = models.CharField(max_length=240, default='',blank=True)
    receiver_name = models.CharField(max_length=30, default='',blank=True)
    interface_line_number = models.CharField(max_length=30, default='',blank=True)
    transaction_type = models.CharField(max_length=25, default='',blank=True)
    auto_transact_code = models.CharField(max_length=25, default='',blank=True)
    transaction_date = models.DateTimeField(auto_now=True)
    source_document_code = models.CharField(max_length=25, default='',blank=True)
    # header_interface_number = models.IntegerField(blank=True, default='0')
    organization_code = models.CharField(max_length=18, default='',blank=True)
    item_number = models.CharField(max_length=300, default='',blank=True)
    document_number = models.CharField(max_length=30, default='',blank=True)
    document_line_number = models.CharField(max_length=18, default='',blank=True)
    document_schedule_number = models.CharField(max_length=18, default='',blank=True)
    document_distribution_number = models.CharField(max_length=18, default='',blank=True)
    sub_inventory_code = models.CharField(max_length=10, default='',blank=True)
    quantity = models.IntegerField(blank=True, default='0')
    po_line_uom = models.CharField(max_length=25, default='',blank=True)
    locator = models.CharField(max_length=81, default='',blank=True)
    interface_source_code = models.CharField(max_length=30, default='',blank=True)

#     # class meta:
#     #     ordering = ['name']
    
#     # def __str__(self):
#     #     return self.name

class InventoryTransaction(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ORGANIZATION_CODE = models.CharField(max_length=18, default='',blank=True)
    SOURCE_CODE = models.CharField(max_length=30, default='',blank=True)
    SOURCE_HEADER_ID = models.IntegerField(blank=True, default='0')
    TRANSACTION_DATE = models.DateTimeField(auto_now=True)
    SOURCE_LINE_ID = models.IntegerField(blank=True, default='0')
    TRANSACTION_COST_IDENTIFIER = models.CharField(max_length=30, default='',blank=True)
    ITEM_NUMBER = models.CharField(max_length=300, default='',blank=True)
    SUBINVENTORY_CODE = models.CharField(max_length=10, default='',blank=True)
    TRANSACTION_QUANTITY = models.IntegerField(blank=True, default='0')
    TRANSACTION_UOM = models.CharField(max_length=3, default='',blank=True)
    TRANSACTION_TYPE_NAME = models.CharField(max_length=30, default='',blank=True)
    TRANSACTION_REFERENCE = models.CharField(max_length=240, default='',blank=True)
    USE_CURRENT_COST = models.CharField(max_length=10, default='N')
    COST_COMPONENT_CODE = models.CharField(max_length=18, default='',blank=True)
    COST = models.IntegerField(blank=True, default='0')

class InventoryMaterial(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movement_request_number = models.IntegerField()
    movement_request_type = models.CharField(max_length=100, default='',blank=True)
    description = models.CharField(max_length=300, default='',blank=True)
    required_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=100, default='',blank=True)
    status = models.CharField(max_length=100, default='',blank=True)
    source_sub_inventory = models.CharField(max_length=100, default='',blank=True)
    source_locator = models.CharField(max_length=100, default='',blank=True)

    destination_sub_inventory = models.CharField(max_length=100, default='',blank=True)
    destination_locator = models.CharField(max_length=100, default='',blank=True)
    destination_account = models.CharField(max_length=100, default='',blank=True)
    line_number = models.IntegerField(blank=True)
    item = models.CharField(max_length=100)
    # transaction_type = models.CharField(max_length=18, default='',blank=True)
    # required_date = models.CharField(max_length=100, default='',blank=True)

    requested_quantity = models.IntegerField()
    uom_name = models.CharField(max_length=100, default='',blank=True)
    # status = models.CharField(max_length=100, default='',blank=True)
    # source_sub_inventory = models.CharField(max_length=100, default='',blank=True)
    # source_locator = models.CharField(max_length=100, default='',blank=True)
    # destination_sub_inventory = models.CharField(max_length=100, default='',blank=True)
    # destination_locator = models.CharField(max_length=100, default='',blank=True)
    # required_date = models.DateTimeField()
    created_by = models.CharField(max_length=100, default='',blank=True)
    # destination_account = models.CharField(max_length=100, default='',blank=True)
