from datetime import datetime
from calendar import timegm
import json

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.utils.timezone import now
#from api.settings import AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME

from .models import (
    CustomUser
)

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'employee_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_no',
            'ic_number',
            'user_type',
            'job_title',
            'status',
            'service_area',
            'crewshift_id',
            'department'
        )
        read_only_fields = ('email', 'id')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    # print('Wikikiki')

    def get_email_options(self):
        # Override this method to change default e-mail options
        print('get_email_options')
        print(self)
        return {
            'subject_template_name': 'password_reset_subject.txt',
            #'email_template_name': 'registration/password_reset_message.txt',
            'html_email_template_name': 'password_reset_message.html',
            # 'extra_email_context': {
            #     'pass_reset_obj': self.pass_reset_obj
            # }
        }
    
    def validate_email(self, value):
        # print('validate_email')
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not CustomUser.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        #
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

