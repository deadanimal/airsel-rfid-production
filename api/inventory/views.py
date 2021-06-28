import json

from django.shortcuts import render
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime

from .models import (
    InventoryItem,
    # InventoryItemUomIntra,
    # InventoryItemUomInter,
    InventoryPurchaseOrder,
    InventoryGrn,
    InventoryTransaction,
    InventoryMaterial
)

from .serializers import (
    InventoryItemSerializer,
    # InventoryItemUomIntraSerializer,
    # InventoryItemUomInterSerializer,
    InventoryPurchaseOrderSerializer,
    InventoryGrnSerializer,
    InventoryTransactionSerializer,
    InventoryMaterialSerializer
)
# Create your views here.

class InventoryItemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = [
    #     'category',
    #     'created_at'
    # ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = InventoryItem.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Asset.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Asset.objects.all()
            else:
                queryset = Asset.objects.filter(company=company.id)
        """
        return queryset

# class InventoryItemUomIntraViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
#     queryset = InventoryItemUomIntra.objects.all()
#     serializer_class = InventoryItemUomIntraSerializer
#     # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     # filterset_fields = [
#     #     'category',
#     #     'created_at'
#     # ]

#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [AllowAny]

#         return [permission() for permission in permission_classes]    

    
#     def get_queryset(self):
#         queryset = InventoryItemUomIntra.objects.all()

#         """
#         if self.request.user.is_anonymous:
#             queryset = Asset.objects.none()

#         else:
#             user = self.request.user
#             company_employee = CompanyEmployee.objects.filter(employee=user)
#             company = company_employee[0].company
            
#             if company.company_type == 'AD':
#                 queryset = Asset.objects.all()
#             else:
#                 queryset = Asset.objects.filter(company=company.id)
#         """
#         return queryset

# class InventoryItemUomInterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
#     queryset = InventoryItemUomInter.objects.all()
#     serializer_class = InventoryItemUomInterSerializer
#     # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     # filterset_fields = [
#     #     'category',
#     #     'created_at'
#     # ]

#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [AllowAny]

#         return [permission() for permission in permission_classes]    

    
#     def get_queryset(self):
#         queryset = InventoryItemUomInter.objects.all()

#         """
#         if self.request.user.is_anonymous:
#             queryset = Asset.objects.none()

#         else:
#             user = self.request.user
#             company_employee = CompanyEmployee.objects.filter(employee=user)
#             company = company_employee[0].company
            
#             if company.company_type == 'AD':
#                 queryset = Asset.objects.all()
#             else:
#                 queryset = Asset.objects.filter(company=company.id)
#         """
#         return queryset

class InventoryPurchaseOrderViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = InventoryPurchaseOrder.objects.all()
    serializer_class = InventoryPurchaseOrderSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = [
    #     'category',
    #     'created_at'
    # ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = InventoryPurchaseOrder.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Asset.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Asset.objects.all()
            else:
                queryset = Asset.objects.filter(company=company.id)
        """
        return queryset

class InventoryGrnViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = InventoryGrn.objects.all()
    serializer_class = InventoryGrnSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = [
    #     'category',
    #     'created_at'
    # ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = InventoryGrn.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Asset.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Asset.objects.all()
            else:
                queryset = Asset.objects.filter(company=company.id)
        """
        return queryset

class InventoryTransactionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = [
    #     'category',
    #     'created_at'
    # ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = InventoryTransaction.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Asset.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Asset.objects.all()
            else:
                queryset = Asset.objects.filter(company=company.id)
        """
        return queryset
        
class InventoryMaterialViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = InventoryMaterial.objects.all()
    serializer_class = InventoryMaterialSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = [
    #     'category',
    #     'created_at'
    # ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = InventoryMaterial.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Asset.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Asset.objects.all()
            else:
                queryset = Asset.objects.filter(company=company.id)
        """
        return queryset
        