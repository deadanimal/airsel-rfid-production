# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from simple_history.models import HistoricalRecords

from core.helpers import PathAndRename

class Media(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')

    MEDIA_TYPE = [
        ('CSV', 'CSV'),
        ('IMG', 'Image'),
        ('EXC', 'Excel')
    ]
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPE, default='IMG')
    document_link = models.FileField(null=True, upload_to=PathAndRename('medias'))

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name