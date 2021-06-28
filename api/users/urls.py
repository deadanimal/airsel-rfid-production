# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

