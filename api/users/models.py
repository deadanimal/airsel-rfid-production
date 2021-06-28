from __future__ import unicode_literals
import json
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from core.helpers import PathAndRename

# from employee.models import Employee

class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_employee_id', default=None, null=True)
    first_name = models.CharField(max_length=255, blank=True, default='NA')
    last_name = models.CharField(max_length=255, blank=True, default='NA')
    ic_number = models.CharField(max_length=14, blank=True, default='NA')
    email = models.EmailField(blank=True, default='NA')
    country = models.CharField(max_length=20, default='Malaysia')
    phone_no = PhoneNumberField(blank=True, null=True)
    job_title = models.CharField(max_length=50, default='NA')
    status = models.BooleanField(default=True)
    service_area = models.CharField(max_length=50, blank=True)
    crewshift_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50, blank=True)
    mobile_access = models.BooleanField(default=True)

    #USER_TYPE = [
    #    ('AM', 'Asset Management System'),
    #    ('IV', 'Inventory'),
    #    ('OP', 'Operator'),
    #    ('SK', 'Store Keeper'),
    #    ('SS', 'Store Supervisor'),
    #    ('TC', 'Technical Crew'),
    #    ('VD', 'Vendor')
    #]

    USER_TYPE = [
        ('AM', 'Admin'),
        ('OP', 'Operator'),
        ('TC', 'Technical Crew'),
        ('CR', 'Contractor'),
        ('PL', 'Planner'),
    ]

    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE,
        default='TC'
    )

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.first_name +' '+ self.last_name

