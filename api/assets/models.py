# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords

from locations.models import (
    Region,
    Location
)

from medias.models import (
    Media
)

from organisations.models import (
    Organisation
)

from users.models import (
    CustomUser
)

from core.helpers import PathAndRename

class Rfid(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    rfid_id = models.CharField(max_length=100, default='NA')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AssetGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    
    CATEGORY = [
        ('AI', 'Asset Identity'),
        ('PG', 'Primary Category'),
        ('S1', 'Sub Category 1'),
        ('S2', 'Sub Category 2')
    ]
    category = models.CharField(max_length=2, choices=CATEGORY, default='AI')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AssetServiceHistory(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_service_history = models.CharField(max_length=100, default='NA')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.asset_service_history

class AssetType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_bussiness_object = models.CharField(max_length=100, default='NA')
    asset_type_code = models.CharField(max_length=100, default='NA')
    asset_type_description = models.CharField(max_length=100, default='NA')
    status = models.CharField(max_length=100, default='NA')
    assessment_class = models.CharField(max_length=100, default='NA')
    profile_failure = models.CharField(max_length=100, default='NA')
    owned_organisation = models.CharField(max_length=100, default='NA')
    instance_organisation = models.CharField(max_length=100, default='NA')

    asset_category = models.CharField(max_length=100, default='')
    # asset_service_history = models.ForeignKey(AssetServiceHistory, on_delete=models.CASCADE, related_name='asset_service_history_asset_service_history_id', null=True)
    asset_service_history = models.ManyToManyField(AssetServiceHistory,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class AssetMeasurementType(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measurement_type = models.CharField(max_length=100, blank=True )
    action_type = models.CharField(max_length=100, blank=True )
    description = models.CharField(max_length=100, blank=True )
    measurement_identifie = models.CharField(max_length=100, blank=True )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.measurement_type

class AssetAttribute(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    characteristic_type = models.CharField(max_length=100, blank=True )
    adhoc_value = models.CharField(max_length=100, blank=True )
    characteristic_value = models.CharField(max_length=100, null=True, blank=True )
    action_type = models.CharField(max_length=100, blank=True )
    characteristic_type_name = models.CharField(max_length=100, null=True, blank=True )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s %s'%(self.characteristic_type, self.adhoc_value, self.characteristic_value))

class Asset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(max_length=12, blank=True )
    asset_type = models.CharField(max_length=100, blank=True )
    transaction_type = models.CharField(max_length=100, blank=True )
    description = models.CharField(max_length=225, blank=True)
    bo = models.CharField(max_length=100, blank=True)
    bo_status = models.CharField(max_length=100, blank=True)
    owning_access_group = models.CharField(max_length=100, null=True, blank=True)
    effective_datetime = models.DateTimeField(null=True)
    node_id = models.CharField(max_length=12, blank=True)
    badge_no = models.CharField(max_length=100, blank=True)
    serial_no = models.CharField(max_length=100, blank=True)
    pallet_no = models.CharField(max_length=100, blank=True)
    handed_over_asset = models.CharField(max_length=100, blank=True)
    fixed_asset_no = models.CharField(max_length=100, blank=True)
    scada_id = models.CharField(max_length=100, blank=True)
    condition_rating = models.CharField(max_length=100, blank=True)
    condifence_rating = models.CharField(max_length=100, blank=True)
    maintenance_specification = models.CharField(max_length=100, blank=True)
    measurement_types = models.ManyToManyField(AssetMeasurementType,blank=True)
    bom_part_id = models.CharField(max_length=100, blank=True)
    attached_to_asset_id = models.CharField(max_length=100, blank=True)
    vehicle_identification_num = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    purchase_order_num = models.CharField(max_length=100, blank=True)
    location_id = models.CharField(max_length=12, blank=True)
    metrology_firmware = models.CharField(max_length=100, blank=True)
    nic_firmware = models.CharField(max_length=100, blank=True)
    configuration = models.CharField(max_length=100, blank=True)
    warranty_expiration_date = models.DateField(null=True)
    warranty_detail = models.CharField(max_length=100, blank=True)
    vendor_part_no = models.CharField(max_length=100, blank=True)
    asset_attributes = models.ManyToManyField(AssetAttribute, blank=True)

    owning_access_group_nam = models.CharField(max_length=100, blank=True)
    specification = models.CharField(max_length=100, blank=True)
    hex_code = models.CharField(max_length=100, blank=True)

    field_1 = models.CharField(max_length=100, blank=True)
    field_2 = models.CharField(max_length=100, blank=True)

    submitted_datetime = models.DateTimeField(null=True, default=None)
    registered_datetime = models.DateTimeField(null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.asset_id

class AssetRegistration(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(max_length=12, default='',null=True, blank=True)
    badge_no = models.CharField(max_length=100, default='',null=True, blank=True)
    node_id = models.CharField(max_length=12, default='',null=True, blank=True)
    hex_code = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_identity = models.CharField(max_length=200, default='',null=True, blank=True)
    parent_location = models.CharField(max_length=200, default='',null=True, blank=True)
    location_description = models.CharField(max_length=200, default='',null=True, blank=True)
    building = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_3 = models.CharField(max_length=200, default='',null=True, blank=True)
    city = models.CharField(max_length=200, default='',null=True, blank=True)
    state = models.CharField(max_length=200, default='',null=True, blank=True)
    postal_code = models.CharField(max_length=200, default='',null=True, blank=True)
    country = models.CharField(max_length=200, default='',null=True, blank=True)
    tag_number = models.CharField(max_length=200, default='',null=True, blank=True)
    service_area = models.CharField(max_length=200, default='',null=True, blank=True)
    location_main_contact = models.CharField(max_length=200, default='',null=True, blank=True)
    location_asset_maintenance_manager = models.CharField(max_length=200, default='',null=True, blank=True)
    maintenance_planner = models.CharField(max_length=200, default='',null=True, blank=True)
    gis_esri_id = models.CharField(max_length=200, default='',null=True, blank=True)
    latitude = models.CharField(max_length=200, default='',null=True, blank=True)
    longitude = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_criticality = models.CharField(max_length=200, default='',null=True, blank=True)
    cost_center = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_owning_department = models.CharField(max_length=200, default='',null=True, blank=True)
    main_operation = models.CharField(max_length=200, default='',null=True, blank=True)
    region = models.CharField(max_length=200, default='',null=True, blank=True)
    operation = models.CharField(max_length=200, default='',null=True, blank=True)
    process_function = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_process_system = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_or_component_type = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_class_asset_category = models.CharField(max_length=200, default='',null=True, blank=True)
    handed_over_asset_or_procured = models.CharField(max_length=200, default='',null=True, blank=True)
    specification = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_primary_category = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_category_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_category_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    brand = models.CharField(max_length=200, default='',null=True, blank=True)
    model_number = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_1_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_2_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_3 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_3_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    attached_to_asset_badge_no = models.CharField(max_length=200, default='',null=True, blank=True)
    attached_to_asset_id = models.CharField(max_length=200, default='',null=True, blank=True)
    detailed_description = models.CharField(max_length=200, default='',null=True, blank=True)
    serial_number = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_tag_number = models.CharField(max_length=200, default='',null=True, blank=True)
    purchase_date_installed_handed_over_date = models.CharField(max_length=200, default='',null=True, blank=True)
    condition_rating = models.CharField(max_length=200, default='',null=True, blank=True)
    status = models.CharField(max_length=200, default='',null=True, blank=True)
    maintenance_specification = models.CharField(max_length=200, default='',null=True, blank=True)
    measurement_type = models.CharField(max_length=200, default='',null=True, blank=True)
    warranty = models.CharField(max_length=200, default='',null=True, blank=True)
    actual_warranty_period = models.CharField(max_length=200, default='',null=True, blank=True)
    warranty_vendor_name = models.CharField(max_length=200, default='',null=True, blank=True)
    bottom_water_level = models.CharField(max_length=200, default='',null=True, blank=True)
    closing_torque = models.CharField(max_length=200, default='',null=True, blank=True)
    dimention = models.CharField(max_length=200, default='',null=True, blank=True)
    frequency = models.CharField(max_length=200, default='',null=True, blank=True)
    infrastructure_status = models.CharField(max_length=200, default='',null=True, blank=True)
    installation = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacturer = models.CharField(max_length=200, default='',null=True, blank=True)
    material_type = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_channel = models.CharField(max_length=200, default='',null=True, blank=True)
    opening_torque = models.CharField(max_length=200, default='',null=True, blank=True)
    pump_head = models.CharField(max_length=200, default='',null=True, blank=True)
    staging_height = models.CharField(max_length=200, default='',null=True, blank=True)
    top_water_level = models.CharField(max_length=200, default='',null=True, blank=True)
    valve_pressure_rating = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_engine_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_auto_windscreen_insured = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_date_period_to = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_sum_insured = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_owner_status = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_puspakom_expired_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_expired_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_seating_capacity = models.CharField(max_length=200, default='',null=True, blank=True)
    communication_protocol = models.CharField(max_length=200, default='',null=True, blank=True)
    environmental_performance = models.CharField(max_length=200, default='',null=True, blank=True)
    horse_power = models.CharField(max_length=200, default='',null=True, blank=True)
    infrastructure_status_reason = models.CharField(max_length=200, default='',null=True, blank=True)
    insulation = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacturer_year = models.CharField(max_length=200, default='',null=True, blank=True)
    model = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_phases = models.CharField(max_length=200, default='',null=True, blank=True)
    outlet_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    revolutions_per_minute = models.CharField(max_length=200, default='',null=True, blank=True)
    supply_location = models.CharField(max_length=200, default='',null=True, blank=True)
    type = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_chasis_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_vendor = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_cover_note_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_no_claim_discount = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_total_premium = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_register_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_permit_date_period_to = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_no_license_operator = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_registration_owner = models.CharField(max_length=200, default='',null=True, blank=True)
    capacity_size = models.CharField(max_length=200, default='',null=True, blank=True)
    coverage_range = models.CharField(max_length=200, default='',null=True, blank=True)
    flow_rate = models.CharField(max_length=200, default='',null=True, blank=True)
    hysteresis = models.CharField(max_length=200, default='',null=True, blank=True)
    inlet_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    legal_name = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacture_part_number = models.CharField(max_length=200, default='',null=True, blank=True)
    motor_current = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_stage = models.CharField(max_length=200, default='',null=True, blank=True)
    power_supply_type = models.CharField(max_length=200, default='',null=True, blank=True)
    source_from = models.CharField(max_length=200, default='',null=True, blank=True)
    temperature = models.CharField(max_length=200, default='',null=True, blank=True)
    valve_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_engine_capacity = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_model = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_date_period_from = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_policy_type = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_puspakom_date_inspection = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_rate = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_renew_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_permit_date_period_from = models.CharField(max_length=200, default='',null=True, blank=True)
    voltage = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_status = models.CharField(max_length=200, default='',null=True, blank=True)

    #Approval
    APPROVAL_STATUS = [
        ('CO', 'Completed'),
        ('IC','Incomplete'),
        ('NP','New Process'),
        ('PR','Processed'),
        ('AP', 'Approved'),
        ('RJ', 'Rejected')
    ]
    status = models.CharField(
        max_length=2,
        choices=APPROVAL_STATUS,
        default='IC'
    )

    bo = models.CharField(max_length=200, default='',null=True, blank=True)
    bo_status = models.CharField(max_length=200, default='',null=True, blank=True)
    new_parent_location = models.CharField(max_length=200, default='',null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class AssetRegistrationBk(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(max_length=12, default='',null=True, blank=True)
    badge_no = models.CharField(max_length=100, default='',null=True, blank=True)
    node_id = models.CharField(max_length=12, default='',null=True, blank=True)
    hex_code = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_identity = models.CharField(max_length=200, default='',null=True, blank=True)
    parent_location = models.CharField(max_length=200, default='',null=True, blank=True)
    location_description = models.CharField(max_length=200, default='',null=True, blank=True)
    building = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    address_line_3 = models.CharField(max_length=200, default='',null=True, blank=True)
    city = models.CharField(max_length=200, default='',null=True, blank=True)
    state = models.CharField(max_length=200, default='',null=True, blank=True)
    postal_code = models.CharField(max_length=200, default='',null=True, blank=True)
    country = models.CharField(max_length=200, default='',null=True, blank=True)
    tag_number = models.CharField(max_length=200, default='',null=True, blank=True)
    service_area = models.CharField(max_length=200, default='',null=True, blank=True)
    location_main_contact = models.CharField(max_length=200, default='',null=True, blank=True)
    location_asset_maintenance_manager = models.CharField(max_length=200, default='',null=True, blank=True)
    maintenance_planner = models.CharField(max_length=200, default='',null=True, blank=True)
    gis_esri_id = models.CharField(max_length=200, default='',null=True, blank=True)
    latitude = models.CharField(max_length=200, default='',null=True, blank=True)
    longitude = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_criticality = models.CharField(max_length=200, default='',null=True, blank=True)
    cost_center = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_owning_department = models.CharField(max_length=200, default='',null=True, blank=True)
    main_operation = models.CharField(max_length=200, default='',null=True, blank=True)
    region = models.CharField(max_length=200, default='',null=True, blank=True)
    operation = models.CharField(max_length=200, default='',null=True, blank=True)
    process_function = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_process_system = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_or_component_type = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_class_asset_category = models.CharField(max_length=200, default='',null=True, blank=True)
    handed_over_asset_or_procured = models.CharField(max_length=200, default='',null=True, blank=True)
    specification = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_primary_category = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_category_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    sub_category_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    brand = models.CharField(max_length=200, default='',null=True, blank=True)
    model_number = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_1 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_1_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_2 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_2_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_3 = models.CharField(max_length=200, default='',null=True, blank=True)
    size_capacity_3_unit_measurement = models.CharField(max_length=200, default='',null=True, blank=True)
    attached_to_asset_badge_no = models.CharField(max_length=200, default='',null=True, blank=True)
    attached_to_asset_id = models.CharField(max_length=200, default='',null=True, blank=True)
    detailed_description = models.CharField(max_length=200, default='',null=True, blank=True)
    serial_number = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_tag_number = models.CharField(max_length=200, default='',null=True, blank=True)
    purchase_date_installed_handed_over_date = models.CharField(max_length=200, default='',null=True, blank=True)
    condition_rating = models.CharField(max_length=200, default='',null=True, blank=True)
    status = models.CharField(max_length=200, default='',null=True, blank=True)
    maintenance_specification = models.CharField(max_length=200, default='',null=True, blank=True)
    measurement_type = models.CharField(max_length=200, default='',null=True, blank=True)
    warranty = models.CharField(max_length=200, default='',null=True, blank=True)
    actual_warranty_period = models.CharField(max_length=200, default='',null=True, blank=True)
    warranty_vendor_name = models.CharField(max_length=200, default='',null=True, blank=True)
    bottom_water_level = models.CharField(max_length=200, default='',null=True, blank=True)
    closing_torque = models.CharField(max_length=200, default='',null=True, blank=True)
    dimention = models.CharField(max_length=200, default='',null=True, blank=True)
    frequency = models.CharField(max_length=200, default='',null=True, blank=True)
    infrastructure_status = models.CharField(max_length=200, default='',null=True, blank=True)
    installation = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacturer = models.CharField(max_length=200, default='',null=True, blank=True)
    material_type = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_channel = models.CharField(max_length=200, default='',null=True, blank=True)
    opening_torque = models.CharField(max_length=200, default='',null=True, blank=True)
    pump_head = models.CharField(max_length=200, default='',null=True, blank=True)
    staging_height = models.CharField(max_length=200, default='',null=True, blank=True)
    top_water_level = models.CharField(max_length=200, default='',null=True, blank=True)
    valve_pressure_rating = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_engine_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_auto_windscreen_insured = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_date_period_to = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_sum_insured = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_owner_status = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_puspakom_expired_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_expired_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_seating_capacity = models.CharField(max_length=200, default='',null=True, blank=True)
    communication_protocol = models.CharField(max_length=200, default='',null=True, blank=True)
    environmental_performance = models.CharField(max_length=200, default='',null=True, blank=True)
    horse_power = models.CharField(max_length=200, default='',null=True, blank=True)
    infrastructure_status_reason = models.CharField(max_length=200, default='',null=True, blank=True)
    insulation = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacturer_year = models.CharField(max_length=200, default='',null=True, blank=True)
    model = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_phases = models.CharField(max_length=200, default='',null=True, blank=True)
    outlet_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    revolutions_per_minute = models.CharField(max_length=200, default='',null=True, blank=True)
    supply_location = models.CharField(max_length=200, default='',null=True, blank=True)
    type = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_chasis_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_vendor = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_cover_note_number = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_no_claim_discount = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_total_premium = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_register_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_permit_date_period_to = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_no_license_operator = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_registration_owner = models.CharField(max_length=200, default='',null=True, blank=True)
    capacity_size = models.CharField(max_length=200, default='',null=True, blank=True)
    coverage_range = models.CharField(max_length=200, default='',null=True, blank=True)
    flow_rate = models.CharField(max_length=200, default='',null=True, blank=True)
    hysteresis = models.CharField(max_length=200, default='',null=True, blank=True)
    inlet_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    legal_name = models.CharField(max_length=200, default='',null=True, blank=True)
    manufacture_part_number = models.CharField(max_length=200, default='',null=True, blank=True)
    motor_current = models.CharField(max_length=200, default='',null=True, blank=True)
    no_of_stage = models.CharField(max_length=200, default='',null=True, blank=True)
    power_supply_type = models.CharField(max_length=200, default='',null=True, blank=True)
    source_from = models.CharField(max_length=200, default='',null=True, blank=True)
    temperature = models.CharField(max_length=200, default='',null=True, blank=True)
    valve_diameter = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_engine_capacity = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_model = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_date_period_from = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_insurance_policy_type = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_puspakom_date_inspection = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_rate = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_roadtax_renew_date = models.CharField(max_length=200, default='',null=True, blank=True)
    vehicle_spad_permit_date_period_from = models.CharField(max_length=200, default='',null=True, blank=True)
    voltage = models.CharField(max_length=200, default='',null=True, blank=True)
    asset_status = models.CharField(max_length=200, default='',null=True, blank=True)

    #Approval
    APPROVAL_STATUS = [
        ('CO', 'Completed'),
        ('IC','Incomplete'),
        ('NP','New Process'),
        ('PR','Processed'),
        ('AP', 'Approved'),
        ('RJ', 'Rejected')
    ]
    status = models.CharField(
        max_length=2,
        choices=APPROVAL_STATUS,
        default='IC'
    )

    bo = models.CharField(max_length=200, default='',null=True, blank=True)
    bo_status = models.CharField(max_length=200, default='',null=True, blank=True)
    new_parent_location = models.CharField(max_length=200, default='',null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class AssetBadgeFormat(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_uuid = models.CharField(max_length=100, default='NA')
    asset_primary_category = models.CharField(max_length=100, default='NA')
    short = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=100, default='NA')

    STATUS_ARRAY = [
        ('AC', 'Active'),
        ('IC','Inactive')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_ARRAY,
        default='IC'
    )
    # status = models.CharField(max_length=100, default='NA')
    latest_no = models.CharField(max_length=100, default='NA')

    skipped_no = ArrayField(models.CharField(max_length=15), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class meta:
        ordering = ['asset_primary_category']
    
    def __str__(self):
        return self.asset_primary_category

class AssetAttributeColumn(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_type_id = models.CharField(max_length=100,default=0)
    bottom_water_level = models.BooleanField(default=False)
    closing_torque = models.BooleanField(default=False)
    dimention = models.BooleanField(default=False)
    frequency = models.BooleanField(default=False)
    infrastructure_status = models.BooleanField(default=False)
    installation = models.BooleanField(default=False)
    manufacturer = models.BooleanField(default=False)
    material_type = models.BooleanField(default=False)
    no_of_channel = models.BooleanField(default=False)
    opening_torque = models.BooleanField(default=False)
    pump_head = models.BooleanField(default=False)
    staging_height = models.BooleanField(default=False)
    top_water_level = models.BooleanField(default=False)
    valve_pressure_rating = models.BooleanField(default=False)
    vehicle_engine_number = models.BooleanField(default=False)
    vehicle_insurance_auto_windscreen_insured = models.BooleanField(default=False)
    vehicle_insurance_date_period_to = models.BooleanField(default=False)
    vehicle_insurance_sum_insured = models.BooleanField(default=False)
    vehicle_owner_status = models.BooleanField(default=False)
    vehicle_puspakom_expired_date = models.BooleanField(default=False)
    vehicle_roadtax_expired_date = models.BooleanField(default=False)
    vehicle_seating_capacity = models.BooleanField(default=False)
    communication_protocol = models.BooleanField(default=False)
    environmental_performance = models.BooleanField(default=False)
    horse_power = models.BooleanField(default=False)
    infrastructure_status_reason = models.BooleanField(default=False)
    insulation = models.BooleanField(default=False)
    manufacturer_year = models.BooleanField(default=False)
    model = models.BooleanField(default=False)
    no_of_phases = models.BooleanField(default=False)
    outlet_diameter = models.BooleanField(default=False)
    revolutions_per_minute = models.BooleanField(default=False)
    supply_location = models.BooleanField(default=False)
    type = models.BooleanField(default=False)
    vehicle_chasis_number = models.BooleanField(default=False)
    vehicle_insurance_vendor = models.BooleanField(default=False)
    vehicle_insurance_cover_note_number = models.BooleanField(default=False)
    vehicle_insurance_no_claim_discount = models.BooleanField(default=False)
    vehicle_insurance_total_premium = models.BooleanField(default=False)
    vehicle_register_date = models.BooleanField(default=False)
    vehicle_spad_permit_date_period_to = models.BooleanField(default=False)
    vehicle_spad_no_license_operator = models.BooleanField(default=False)
    vehicle_registration_owner = models.BooleanField(default=False)
    capacity_size = models.BooleanField(default=False)
    coverage_range = models.BooleanField(default=False)
    flow_rate = models.BooleanField(default=False)
    hysteresis = models.BooleanField(default=False)
    inlet_diameter = models.BooleanField(default=False)
    legal_name = models.BooleanField(default=False)
    manufacture_part_number = models.BooleanField(default=False)
    motor_current = models.BooleanField(default=False)
    no_of_stage = models.BooleanField(default=False)
    power_supply_type = models.BooleanField(default=False)
    source_from = models.BooleanField(default=False)
    temperature = models.BooleanField(default=False)
    valve_diameter = models.BooleanField(default=False)
    vehicle_engine_capacity = models.BooleanField(default=False)
    vehicle_model = models.BooleanField(default=False)
    vehicle_insurance_date_period_from = models.BooleanField(default=False)
    vehicle_insurance_policy_type = models.BooleanField(default=False)
    vehicle_puspakom_date_inspection = models.BooleanField(default=False)
    vehicle_roadtax_rate = models.BooleanField(default=False)
    vehicle_roadtax_renew_date = models.BooleanField(default=False)
    vehicle_spad_permit_date_period_from = models.BooleanField(default=False)
    voltage = models.BooleanField(default=False)
    asset_status = models.BooleanField(default=False)
    brand = models.BooleanField(default=False)

    model_number = models.BooleanField(default=False)
    bo = models.BooleanField(default=False)
    bo_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-asset_type_id']

class AssetLocation(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    location_type = models.CharField(max_length=100, blank=True)
    locatin_disposition = models.CharField(max_length=100, blank=True)
    Bo = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    parent_loc_or_org = models.CharField(max_length=100, blank=True)
    work_request_approval_profile = models.CharField(max_length=100, blank=True)
    owning_org = models.CharField(max_length=100, blank=True)

    building = models.CharField(max_length=100, blank=True)
    room = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address_1 = models.CharField(max_length=100, blank=True)
    address_2 = models.CharField(max_length=100, blank=True)
    address_3 = models.CharField(max_length=100, blank=True)
    cross_street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    suburb = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=100, blank=True)
    location_class = models.CharField(max_length=100, blank=True)

    main_contact = models.CharField(max_length=100, blank=True)
    maintenance_manager = models.CharField(max_length=100, blank=True)
    planner = models.CharField(max_length=100, blank=True)
    cost_center = models.CharField(max_length=100, blank=True)

    rcm_system = models.CharField(max_length=100, blank=True)
    environmental_rating = models.CharField(max_length=100, blank=True)
    service_condition = models.CharField(max_length=100, blank=True)
    duty_cycle = models.CharField(max_length=100, blank=True)
    backlog_group = models.CharField(max_length=100, blank=True)
    run_to_failure = models.CharField(max_length=100, blank=True)
    breaker = models.CharField(max_length=100, blank=True)
    runtime_source = models.CharField(max_length=100, blank=True)
    tag_number = models.CharField(max_length=100, blank=True)
    site_location = models.CharField(max_length=100, blank=True)
    point_id = models.CharField(max_length=100, blank=True)
    service_area = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    asset_criticality = models.CharField(max_length=100, blank=True)
    criticality_reason = models.CharField(max_length=100, blank=True)
    gis_id = models.CharField(max_length=100, blank=True)
    connected_to_location_id = models.CharField(max_length=12, blank=True)
    water_asset_category = models.CharField(max_length=100, blank=True)
    land_asset_status = models.CharField(max_length=100, blank=True)
    land_ownership_number = models.CharField(max_length=100, blank=True)
    take_over_date = models.DateField(null=True)
    take_over_date_source_qt11 = models.DateField(null=True)
    take_over_date_source_ccc = models.DateField(null=True)
    land_area_acre = models.CharField(max_length=100, blank=True)
    plan_certified_number = models.CharField(max_length=100, blank=True)
    plan_pre_computation_number = models.CharField(max_length=100, blank=True)
    plan_as_built_number = models.CharField(max_length=100, blank=True)
    quit_rent_bill_number = models.CharField(max_length=100, blank=True)
    current_rate_of_quit_rent = models.CharField(max_length=100, blank=True)
    quit_rent_bill_payment_date = models.DateField(null=True)
    assessment_bill_number = models.CharField(max_length=100, blank=True)
    current_rate_Of_assesment = models.CharField(max_length=100, blank=True)
    assessment_bill_payment_date = models.DateField(null=True)
    lease_expired_date = models.DateField(null=True)
    remarks = models.CharField(max_length=100, blank=True)

    parent_location_name = models.CharField(max_length=100, blank=True)
    main_contact_name = models.CharField(max_length=100, blank=True)
    maintenance_manager_nam = models.CharField(max_length=100, blank=True)
    planner_name = models.CharField(max_length=100, blank=True)

    field_1 = models.CharField(max_length=100, blank=True)
    field_2 = models.CharField(max_length=100, blank=True)

    submitted_datetime = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.work_request_approval_profile

## baru tambah
class AssetLocationSync(models.Model):

    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    node_id = models.CharField(max_length=12, blank=True)
    description = models.CharField(max_length=255, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class AssetAttributeField(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_type_id = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, blank=True )
    value = models.CharField(max_length=100, blank=True )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    # def __str__(self):
    #     return ('%s %s %s'%(self.characteristic_type, self.adhoc_value, self.characteristic_value))

class AssetMeasurementTypeInbound(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measurement_type = models.CharField(max_length=100, blank=True )
    action_type = models.CharField(max_length=100, blank=True )
    description = models.CharField(max_length=250, blank=True )
    measurement_identifie = models.CharField(max_length=100, blank=True )
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset_measurement_type_inbound_asset_id', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.measurement_type

class AssetAttributeInbound(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    characteristic_type = models.CharField(max_length=100, blank=True )
    adhoc_value = models.CharField(max_length=100, blank=True )
    characteristic_value = models.CharField(max_length=100, null=True)
    action_type = models.CharField(max_length=100, blank=True )
    characteristic_type_name = models.CharField(max_length=100, null=True)
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset_attribute_inbound_asset_id', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s %s'%(self.characteristic_type, self.adhoc_value, self.characteristic_value))

class AssetMaintenanceSpec(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maintenance_spec_cd = models.CharField(max_length=100, blank=True)
    asset_type_cd = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return (self.maintenance_spec_cd)

class AssetAttributeReference(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    char_type_cd = models.CharField(max_length=100, blank=True)
    attribute_field_name = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return (self.char_type_cd)

class AssetAttributePredefine(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_field_name = models.CharField(max_length=100, blank=True)
    characteristic_value = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return (self.attribute_field_name)
