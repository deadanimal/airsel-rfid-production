from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import os

from django.views.generic import View
from django.template import Context, Template

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()

from django.core.mail import send_mail

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['user_type'] = user.user_type

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from django.shortcuts import render
from django.db.models import Q

from django.contrib.sites.models import Site
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CustomUser
)

from .serializers import (
    CustomUserSerializer
)

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.status = True
            user.save()

        else:
            #messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            user.is_active = True
            user.status = True
            user.save()
        
        html = "<html><body>Your Account Has Been Activated</body></html>"
        return HttpResponseRedirect("https://airsel-rfid.pipe.my/")

class CustomUserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'user_type',
        'employee_id','username','email',
        'is_active'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = CustomUser.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = User.objects.all()
            else:
                queryset = User.objects.filter(company=company.id)
        """
        return queryset    

    @action(methods=['POST'], detail=False)
    def activation(self, request):
        #check request

        pk = request.data['user_pk']
        user = CustomUser.objects.all().filter(email=pk)[0]
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        print("USER", user, uid, token, user.username)


        # Email
        current_site = get_current_site(request)
        current_site = Site.objects.get_current()

        #domain = "127.0.0.1:8000"
        domain = "airsel-rfid-api-prod.pipe.my"

        subject = 'Activate Your Account'
        message = render_to_string(f'{BASE_DIR}/templates/account/email/email_confirmation_message.html', {
            # comment this line before push to repo
            # uncomment this line when going live
            #domain : "http://airsel-rfid-api-prod.pipe.my/"

            'uid': uid,
            'token': token,
            'username': user.username,
            'password': 'bg6yaaz3pv',
            'url': f"http://{domain}/activate/{uid}/{token}/"
        })

        to = [user.email]
        send_mail(subject, message, None, to, fail_silently=False)
        user.email_user(subject, message)

        return Response({})

