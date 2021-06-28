# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid, datetime

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

from simple_history.models import HistoricalRecords

from assets.models import (
    Asset
)
from medias.models import (
    Media
)
from users.models import (
    CustomUser
)

from core.helpers import PathAndRename

# Create your models here.

class Employee(models.Model):

    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_no = models.CharField(max_length=100, blank=True)
    ic_number = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    service_area = models.CharField(max_length=100, blank=True)
    crewshift_id = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    bo_status_cd = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    business_unit_cd = models.CharField(max_length=100, blank=True)
    hr_employee_number = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    staff_no = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    error = models.CharField(max_length=100, blank=True)
    errorMessage = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    time = models.CharField(max_length=100, blank=True)
    hash = models.CharField(max_length=100, blank=True)
    is_wams = models.CharField(max_length=100, blank=True)
    is_ad = models.CharField(max_length=100, blank=True)
    is_erp = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s %s'%(self.first_name, self.last_name,self.employee_id))

class FailureProfile(models.Model):

    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    failure_profile = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    failure_repair = models.CharField(max_length=100, blank=True)
    failure_mode = models.CharField(max_length=100, blank=True)
    failure_comp = models.CharField(max_length=100, blank=True)
    failure_type = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class ApprovalProfile(models.Model):

    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    approval_profile = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=250, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class ContactInformation(models.Model):

    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_id = models.CharField(max_length=250, blank=True)
    # employee_id = models.CharField(max_length=250, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contact_information_employee_id', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']
