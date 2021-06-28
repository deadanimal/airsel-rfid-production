import uuid
from django.db import models

class AuditTrail(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    action = models.CharField(max_length=200, default='NA')
    created_at = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['created_at']


