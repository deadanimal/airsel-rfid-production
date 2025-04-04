# Generated by Django 2.2.6 on 2021-06-28 06:39

import core.helpers
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NA', max_length=100)),
                ('media_type', models.CharField(choices=[('CSV', 'CSV'), ('IMG', 'Image'), ('EXC', 'Excel')], default='IMG', max_length=3)),
                ('document_link', models.FileField(null=True, upload_to=core.helpers.PathAndRename('medias'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
