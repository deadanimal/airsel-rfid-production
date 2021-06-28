# Generated by Django 2.2.6 on 2021-06-28 06:39

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, default='NA', max_length=255)),
                ('last_name', models.CharField(blank=True, default='NA', max_length=255)),
                ('ic_number', models.CharField(blank=True, default='NA', max_length=14)),
                ('email', models.EmailField(blank=True, default='NA', max_length=254)),
                ('country', models.CharField(default='Malaysia', max_length=20)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('job_title', models.CharField(default='NA', max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('service_area', models.CharField(blank=True, max_length=50)),
                ('crewshift_id', models.CharField(blank=True, max_length=50)),
                ('department', models.CharField(blank=True, max_length=50)),
                ('mobile_access', models.BooleanField(default=True)),
                ('user_type', models.CharField(choices=[('AM', 'Admin'), ('OP', 'Operator'), ('TC', 'Technical Crew'), ('CR', 'Contractor'), ('PL', 'Planner')], default='TC', max_length=2)),
                ('employee_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_customuser_employee_id', to='employee.Employee')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
