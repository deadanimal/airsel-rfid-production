import json

from django.shortcuts import render
from django.db.models import F, Q, Count

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin

from core.utils import convert_gmt8_to_utc0
from itertools import chain
from datetime import datetime
import json
import pytz

from wams.services.int10_inboundworkrequest import get_inboundworkrequest

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    OwningOrganization,
    Bo,
    Maintenance,
    IssueType,
    WorkOrder,
    WorkActivity,
    WorkActivityTeam,
    WorkClass,
    WorkCategory,
    WorkRequest,
    WorkRequestStatus,
    MeasurementType,
    OperationalReading,
    WorkOrderActivityCompletionAssetLocationAssetList,
    AssetLocationAssetListServiceHistories,
    ServiceHistoriesQuestions,
    QuestionsValidValue,
    WorkOrderActivityCompletion,
    ServiceHistory, ServiceHistoryQuestion, ServiceHistoryQuestionValidValue,
    Planner, MaintenanceManager, WorkRequest, MainOperation, Function, LocationType,
    SubFunction, CostCenter, Operation, WorkActivityEmployee,
    WorkOrderActivityCompletionAssetLocationAssetListInbound,
    AssetLocationAssetListServiceHistoriesInbound
)

from .serializers import (
    OwningOrganizationSerializer,
    OwningOrganizationExtendedSerializer,
    BoSerializer,
    BoExtendedSerializer,
    MaintenanceSerializer,
    IssueTypeSerializer,
    WorkOrderSerializer,
    WorkActivitySerializer,
    WorkActivityExtendedSerializer,
    WorkActivityTeamSerializer,
    WorkClassSerializer,
    WorkClassExtendedSerializer,
    WorkCategorySerializer,
    WorkCategoryExtendedSerializer,
    WorkRequestSerializer,
    WorkRequestExtendedSerializer,
    WorkRequestStatusSerializer,
    # WorkRequestStatusExtendedSerializer,
    MeasurementTypeSerializer,
    MeasurementTypeExtendedSerializer,
    OperationalReadingSerializer,
    OperationalReadingExtendedSerializer,
    WorkOrderActivityCompletionAssetLocationAssetListSerializer,
    AssetLocationAssetListServiceHistoriesSerializer,
    ServiceHistoriesQuestionsSerializer,
    QuestionsValidValueSerializer,
    WorkOrderActivityCompletionSerializer,
    WorkOrderActivityCompletionExtendedSerializer,
    ServiceHistorySerializer, ServiceHistoryQuestionSerializer, ServiceHistoryQuestionValidValueSerializer,
    PlannerSerializer, MaintenanceManagerSerializer, WorkRequestSerializer, MainOperationSerializer, FunctionSerializer, LocationTypeSerializer,
    SubFunctionSerializer, CostCenterSerializer, OperationSerializer, WorkActivityEmployeeSerializer,
    WorkOrderActivityCompletionAssetLocationAssetListInboundSerializer,
    AssetLocationAssetListServiceHistoriesInboundSerializer,
    # WorkOrderActivityCompletionPipeSerializer,
    WorkRequestPipeSerializer,
    OperationalReadingPipeSerializer
)

from users.models import CustomUser

from employee.models import Employee


class OwningOrganizationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = OwningOrganization.objects.all()
    serializer_class = OwningOrganizationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'name', 'description', 'detail_description', 'record_by', 'modified_by'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = OwningOrganization.objects.all()
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = OwningOrganization.objects.all()
        serializer_class = OwningOrganizationExtendedSerializer(
            queryset, many=True)

        return Response(serializer_class.data)


class BoViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Bo.objects.all()
    serializer_class = BoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'name', 'description', 'status', 'record_by', 'modified_by'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Bo.objects.all()
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = Bo.objects.all()
        serializer_class = BoExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)


class MaintenanceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'created_at'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Maintenance.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Activity.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset


class IssueTypeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = IssueType.objects.all()
    serializer_class = IssueTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'created_at'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = IssueType.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Activity.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset


class WorkOrderViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'completed_at',
        'planner_name',
        'wams_id',
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkOrder.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset


class WorkActivityViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkActivity.objects.all()
    serializer_class = WorkActivitySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'record_date',
        'record_by'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkActivity.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = WorkActivity.objects.all()
        serializer_class = WorkActivityExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)


class WorkActivityTeamViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkActivityTeam.objects.all()
    serializer_class = WorkActivityTeamSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'work_activity',
        'teammate',
        'created_at'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkActivityTeam.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset


class WorkClassViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkClass.objects.all()
    serializer_class = WorkClassSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'name', 'description', 'record_by', 'modified_by'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkClass.objects.all()
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = WorkClass.objects.all()
        serializer_class = WorkClassExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)


class WorkCategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkCategory.objects.all()
    serializer_class = WorkCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'work_category'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkCategory.objects.all()
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = WorkCategory.objects.all()
        serializer_class = WorkCategoryExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)


class WorkRequestViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkRequest.objects.all()
    serializer_class = WorkRequestSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'long_description', 'node_id', 'asset_id', 'required_by_date'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkRequest.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset

    def create(self, request):

        request.data['creation_datetime'] = datetime.now(pytz.utc).replace(microsecond=0).isoformat()
        request.data['downtime_start'] = convert_gmt8_to_utc0(request.data['downtime_start'])

        data = {
            'description': request.data['description'], 
            'long_description': request.data['long_description'],
            'required_by_date': request.data['required_by_date'], 
            'approval_profile': request.data['approval_profile'], 
            'bo': request.data['bo'], 
            'creation_datetime': request.data['creation_datetime'], 
            'creation_user': request.data['creation_user'], 
            'downtime_start': request.data['downtime_start'], 
            'planner': request.data['planner'], 
            'work_class': request.data['work_class'], 
            'work_category': request.data['work_category'], 
            'work_priority': request.data['work_priority'], 
            'requestor': request.data['requestor'], 
            'owning_access_group': request.data['owning_access_group'], 
            'first_name': request.data['first_name'], 
            'last_name': request.data['last_name'], 
            'primary_phone': request.data['primary_phone'], 
            'mobile_phone': request.data['mobile_phone'], 
            'home_phone': request.data['home_phone'], 
            'node_id': request.data['node_id'], 
            'asset_id': request.data['asset_id']
        }

        middleware_call = get_inboundworkrequest('create', data)
        print('middleware_call', middleware_call)
        
        if middleware_call['status'] == 'CREATED':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            wr_update = WorkRequest.objects.get(id=serializer.data['id'])
            wr_update.work_request_id = middleware_call['work_request_id']
            wr_update.work_request_status = middleware_call['status']
            wr_update.save()

            wr_response = WorkRequest.objects.filter(id=serializer.data['id']).values()

            return Response(wr_response[0], status=status.HTTP_201_CREATED, headers=headers)

        elif middleware_call['status'] == 'ERROR':
            return Response({'error_details': middleware_call['error_details']}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def submit_approval_profile(self, request, *args, **kwargs):

        data = json.loads(request.body)
        print('data', data)

        wr_update = WorkRequest.objects.get(id=data['id'], work_request_id=data['work_request_id'])
        wr_update.approval_profile = data['approval_profile']
        wr_update.work_request_status = 'PENDAPPROVAL'
        wr_update.save()

        request = {
            'work_request_id': data['work_request_id'],
            'approval_profile': data['approval_profile'],
            'work_request_status': 'PENDAPPROVAL'
        }

        middleware_call = get_inboundworkrequest('update', request)
        print('middleware_call', middleware_call)

        if middleware_call['status'] == 'SUCCESS':
            wr_update = WorkRequest.objects.get(id=data['id'], work_request_id=data['work_request_id'])
            wr_update.work_request_status = middleware_call['status']
            wr_update.save()

            wr_response = WorkRequest.objects.filter(id=data['id']).values()

            return Response(wr_response[0], status=status.HTTP_201_CREATED)

        elif middleware_call['status'] == 'ERROR':
            return Response({'error_details': middleware_call['error_details']}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = WorkRequest.objects.all()
        serializer_class = WorkRequestExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)

    @action(methods=['POST'], detail=False)
    def desc_ordered_list(self, request, *args, **kwargs):
        
        userid = self.request.data['userid']
        
        # queryset = OperationalReading.objects.values('id','description','long_description','required_by_date','approval_profile','bo','creation_datetime','creation_user','downtime_start','planner','work_class','work_category','work_priority','requestor','owning_access_group','first_name','last_name','primary_phone','mobile_phone','home_phone','node_id','asset_id','status','int10_type','work_request_id','work_request_status','created_date','modified_date').order_by('-modified_date')
        # queryset = WorkRequest.objects.all().order_by('-modified_date')
        queryset = WorkRequest.objects.filter(record_by=userid).order_by('-modified_date')
        serializer_class = WorkRequestSerializer(
            queryset, many=True)

        return Response(serializer_class.data)


class WorkRequestPipeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkRequest.objects.all()
    serializer_class = WorkRequestPipeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'long_description', 'node_id', 'asset_id', 'required_by_date'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkRequest.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = Activity.objects.all()
            else:
                queryset = Activity.objects.filter(company=company.id)
        """
        return queryset

    def create(self, request):

        request.data['creation_datetime'] = datetime.now(pytz.utc).replace(microsecond=0).isoformat()
        request.data['downtime_start'] = convert_gmt8_to_utc0(request.data['downtime_start'])

        data = {
            'description': request.data['description'], 
            'long_description': request.data['long_description'],
            'required_by_date': request.data['required_by_date'], 
            'approval_profile': request.data['approval_profile'], 
            'bo': request.data['bo'], 
            'creation_datetime': request.data['creation_datetime'], 
            'creation_user': request.data['creation_user'], 
            'downtime_start': request.data['downtime_start'], 
            'planner': request.data['planner'], 
            'work_class': request.data['work_class'], 
            'work_category': request.data['work_category'], 
            'work_priority': request.data['work_priority'], 
            'requestor': request.data['requestor'], 
            'owning_access_group': request.data['owning_access_group'], 
            'first_name': request.data['first_name'], 
            'last_name': request.data['last_name'], 
            'primary_phone': request.data['primary_phone'], 
            'mobile_phone': request.data['mobile_phone'], 
            'home_phone': request.data['home_phone'], 
            'node_id': request.data['node_id'], 
            'asset_id': request.data['asset_id']
        }

        middleware_call = get_inboundworkrequest('create', data)
        print('middleware_call', middleware_call)
        
        if middleware_call['status'] == 'CREATED':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            wr_update = WorkRequest.objects.get(id=serializer.data['id'])
            wr_update.work_request_id = middleware_call['work_request_id']
            wr_update.work_request_status = middleware_call['status']
            wr_update.save()

            wr_response = WorkRequest.objects.filter(id=serializer.data['id']).values()

            return Response(wr_response[0], status=status.HTTP_201_CREATED, headers=headers)

        elif middleware_call['status'] == 'ERROR':
            return Response({'error_details': middleware_call['error_details']}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def submit_approval_profile(self, request, *args, **kwargs):

        data = json.loads(request.body)
        print('data', data)

        wr_update = WorkRequest.objects.get(id=data['id'], work_request_id=data['work_request_id'])
        wr_update.approval_profile = data['approval_profile']
        wr_update.work_request_status = 'PENDAPPROVAL'
        wr_update.save()

        request = {
            'work_request_id': data['work_request_id'],
            'approval_profile': data['approval_profile'],
            'work_request_status': 'PENDAPPROVAL'
        }

        middleware_call = get_inboundworkrequest('update', request)
        print('middleware_call', middleware_call)

        if middleware_call['status'] == 'SUCCESS':
            wr_update = WorkRequest.objects.get(id=data['id'], work_request_id=data['work_request_id'])
            wr_update.work_request_status = middleware_call['status']
            wr_update.save()

            wr_response = WorkRequest.objects.filter(id=data['id']).values()

            return Response(wr_response[0], status=status.HTTP_201_CREATED)

        elif middleware_call['status'] == 'ERROR':
            return Response({'error_details': middleware_call['error_details']}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = WorkRequest.objects.all()
        serializer_class = WorkRequestExtendedSerializer(queryset, many=True)

        return Response(serializer_class.data)

    @action(methods=['POST'], detail=False)
    def desc_ordered_list(self, request, *args, **kwargs):
        
        userid = self.request.data['userid']
        print("userid=======",userid)
        # queryset = OperationalReading.objects.values('id','description','long_description','required_by_date','approval_profile','bo','creation_datetime','creation_user','downtime_start','planner','work_class','work_category','work_priority','requestor','owning_access_group','first_name','last_name','primary_phone','mobile_phone','home_phone','node_id','asset_id','status','int10_type','work_request_id','work_request_status','created_date','modified_date').order_by('-modified_date')
        # queryset = WorkRequest.objects.all().order_by('-modified_date')
        queryset = WorkRequest.objects.filter(record_by=userid).order_by('-modified_date')
        serializer_class = WorkRequestPipeSerializer(
            queryset, many=True)

        return Response(serializer_class.data)



class WorkRequestStatusViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkRequestStatus.objects.all()
    serializer_class = WorkRequestStatusSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'work_request_id', 'status'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkRequestStatus.objects.all()
        return queryset

    # @action(methods=['GET'], detail=False)
    # def extended(self, request, *args, **kwargs):

    #     queryset = WorkRequestStatus.objects.all()
    #     serializer_class = WorkRequestStatusExtendedSerializer(
    #         queryset, many=True)

    #     return Response(serializer_class.data)


class MeasurementTypeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = []

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = MeasurementType.objects.all()
        return queryset

    @action(methods=['GET'], detail=False)
    def extended(self, request, *args, **kwargs):

        queryset = MeasurementType.objects.all()
        serializer_class = MeasurementTypeExtendedSerializer(
            queryset, many=True)

        return Response(serializer_class.data)


class OperationalReadingViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = OperationalReading.objects.all()
    serializer_class = OperationalReadingSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_id', 'badge_number'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = OperationalReading.objects.all()

        # FROM APPLICATION/JSON THROUGH API
        if bool(self.request.data):
            print("enter bool()")
            if 'from_date' in self.request.data and 'to_date' in self.request.data:

                from_date = self.request.data.get('from_date', None)
                to_date = self.request.data.get('to_date', None)

                if from_date is not None and to_date is not None:
                    # print(OperationalReading.objects.filter(submitted_datetime__range=(from_date,to_date)).query)
                    queryset = OperationalReading.objects.filter(
                        submitted_datetime__range=(from_date, to_date))

        return queryset

    @action(methods=['POST'], detail=False)
    def extended_all(self, request, *args, **kwargs):

        from_date = self.request.data['from_date']
        to_date = self.request.data['to_date']

        if from_date is not None and to_date is not None:
            queryset = OperationalReading.objects.filter(
                submitted_datetime__range=(from_date, to_date))

        serializer = OperationalReadingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # @action(methods=['GET'], detail=False)
    # def asc_ordered_list(self, request, *args, **kwargs):

    #     queryset = OperationalReading.objects.all()
    #     serializer_class = MeasurementTypeExtendedSerializer(
    #         queryset, many=True)

    #     return Response(serializer_class.data)

    @action(methods=['POST'], detail=False)
    def asc_ordered_list(self, request, *args, **kwargs):
        
        userid = self.request.data['userid']
        
        # queryset = OperationalReading.objects.values('id','description','long_description','required_by_date','approval_profile','bo','creation_datetime','creation_user','downtime_start','planner','work_class','work_category','work_priority','requestor','owning_access_group','first_name','last_name','primary_phone','mobile_phone','home_phone','node_id','asset_id','status','int10_type','work_request_id','work_request_status','created_date','modified_date').order_by('-modified_date')
        # queryset = OperationalReading.objects.all().order_by('-modified_date')
        queryset = OperationalReading.objects.filter(record_by=userid).order_by('-modified_date')

        serializer_class = OperationalReadingSerializer(
            queryset, many=True)

        return Response(serializer_class.data)


class OperationalReadingPipeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = OperationalReading.objects.all()
    serializer_class = OperationalReadingPipeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_id', 'badge_number'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = OperationalReading.objects.all()

        # FROM APPLICATION/JSON THROUGH API
        if bool(self.request.data):
            print("enter bool()")
            if 'from_date' in self.request.data and 'to_date' in self.request.data:

                from_date = self.request.data.get('from_date', None)
                to_date = self.request.data.get('to_date', None)

                if from_date is not None and to_date is not None:
                    # print(OperationalReading.objects.filter(submitted_datetime__range=(from_date,to_date)).query)
                    queryset = OperationalReading.objects.filter(
                        submitted_datetime__range=(from_date, to_date))

        return queryset

    @action(methods=['POST'], detail=False)
    def extended_all(self, request, *args, **kwargs):

        from_date = self.request.data['from_date']
        to_date = self.request.data['to_date']

        if from_date is not None and to_date is not None:
            queryset = OperationalReading.objects.filter(
                submitted_datetime__range=(from_date, to_date))

        serializer = OperationalReadingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # @action(methods=['GET'], detail=False)
    # def asc_ordered_list(self, request, *args, **kwargs):

    #     queryset = OperationalReading.objects.all()
    #     serializer_class = MeasurementTypeExtendedSerializer(
    #         queryset, many=True)

    #     return Response(serializer_class.data)

    @action(methods=['POST'], detail=False)
    def asc_ordered_list(self, request, *args, **kwargs):
        
        userid = self.request.data['userid']
        
        # queryset = OperationalReading.objects.values('id','description','long_description','required_by_date','approval_profile','bo','creation_datetime','creation_user','downtime_start','planner','work_class','work_category','work_priority','requestor','owning_access_group','first_name','last_name','primary_phone','mobile_phone','home_phone','node_id','asset_id','status','int10_type','work_request_id','work_request_status','created_date','modified_date').order_by('-modified_date')
        # queryset = OperationalReading.objects.all().order_by('-modified_date')
        queryset = OperationalReading.objects.filter(record_by=userid).order_by('-modified_date')

        serializer_class = OperationalReadingSerializer(
            queryset, many=True)

        return Response(serializer_class.data)


# start copied from dev api


class WorkOrderActivityCompletionAssetLocationAssetListViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkOrderActivityCompletionAssetLocationAssetList.objects.all()
    serializer_class = WorkOrderActivityCompletionAssetLocationAssetListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkOrderActivityCompletionAssetLocationAssetList.objects.all()

        return queryset


class AssetLocationAssetListServiceHistoriesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetLocationAssetListServiceHistories.objects.all()
    serializer_class = AssetLocationAssetListServiceHistoriesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = AssetLocationAssetListServiceHistories.objects.all()

        return queryset


class ServiceHistoriesQuestionsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ServiceHistoriesQuestions.objects.all()
    serializer_class = ServiceHistoriesQuestionsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = ServiceHistoriesQuestions.objects.all()

        return queryset


class QuestionsValidValueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = QuestionsValidValue.objects.all()
    serializer_class = QuestionsValidValueSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = QuestionsValidValue.objects.all()

        return queryset

# class WorkOrderActivityCompletionPipeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
#     queryset = WorkOrderActivityCompletion.objects.all()
#     serializer_class = WorkOrderActivityCompletionPipeSerializer
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_fields = [
#         'activityid', 'bo_status_cd', 'act_type_cd', 'service_class_cd', 'descr100','descrlong','field_1','field_2','status','owning_organization','record_by','modified_by'
#     ]

#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [AllowAny]

#         return [permission() for permission in permission_classes]

#     def get_queryset(self):
#         queryset = WorkOrderActivityCompletion.objects.all()

#         # FROM APPLICATION/JSON THROUGH API
#         if bool(self.request.data):
#             print("enter bool()")
#             if 'from_date' in self.request.data and 'to_date' in self.request.data:

#                 from_date = self.request.data.get('from_date', None)
#                 to_date = self.request.data.get('to_date', None)

#                 if from_date is not None and to_date is not None:
#                     # print(WorkOrderActivityCompletion.objects.filter(submitted_datetime__range=(from_date,to_date)).query)
#                     queryset = WorkOrderActivityCompletion.objects.filter(
#                         submitted_datetime__range=(from_date, to_date))

#         return queryset

#     @action(methods=['POST'], detail=False)
#     def extended_all(self, request, *args, **kwargs):

#         from_date = self.request.data['from_date']
#         to_date = self.request.data['to_date']

#         queryset = WorkOrderActivityCompletion.objects.all()

#         if from_date is not None and to_date is not None:
#             queryset = WorkOrderActivityCompletion.objects.filter(
#                 submitted_datetime__range=(from_date, to_date))

#         serializer = WorkOrderActivityCompletionExtendedSerializer(
#             queryset, many=True)
#         return Response(serializer.data)

#     @action(methods=['GET'], detail=True)
#     def extended(self, request, *args, **kwargs):
#         work_order_activity = self.get_object()

#         serializer = WorkOrderActivityCompletionExtendedSerializer(
#             work_order_activity)
#         return Response(serializer.data)

#     # @action(methods=['GET'], detail=False)
#     @action(methods=['POST'], detail=False)
#     def asc_ordered_list(self, request, *args, **kwargs):
        
#         userid = self.request.data['userid']
#         user_details = CustomUser.objects.filter(id=userid).values('employee_id')

#         # print(user_details)
#         emp_id = ''

#         for i in user_details:
#             emp_id = i['employee_id']

#         work_act_emp = WorkActivityEmployee.objects.filter(employee_id=emp_id).values('work_order_activity_completion_id').order_by('created_date')
#         # print("work_act_emp",work_act_emp)

#         work_order_act_comp = []
#         no = 0
#         for j in work_act_emp:
#             print("work_act_emp------------------",j['work_order_activity_completion_id'])
#             print("no -- ",no)
#             # if no <= 1:
#             woac_det = WorkOrderActivityCompletion.objects.filter(id=j['work_order_activity_completion_id']).values('id','activityid','completiondatetime','bo_status_cd','user_id_1','act_type_cd','wo_id','act_dpos_flg','service_class_cd','requestor_id','required_by_dt','work_priority_flg','descr100','descrlong','w1_descr100_upr','held_for_parts_flg','anniversary_value','emergency_flg','act_num','planner_cd','total_priority','total_priority_src_flg','node_id_1','asset_id_1','percentage','seqno','participation_flg','cost_center_cd','percentage_2','act_resrc_reqmt_id','descrlong_1','resrc_src_flg','resrc_type_id','w1_quantity','unit_price','w1_duration','crew_shift_id','sched_duration','break_in_dttm','actvn_dttm','tmpl_act_id','maint_sched_id','maint_sched_id','status','owning_organization','field_1','field_2','submitted_datetime','created_date','modified_date','record_by','modified_by','asset_location_asset_list')
#             # woac_det = WorkOrderActivityCompletion.objects.get(id=j['work_order_activity_completion_id']).values_list()
#             work_order_act_comp.insert(no,woac_det[0])
        
#             # print(woac_det)
#             print(woac_det[0])

#             no = no + 1

#         # print("work_order_act_comp>>>>>>>",work_order_act_comp)
#         # queryset = OperationalReading.objects.values('id','description','long_description','required_by_date','approval_profile','bo','creation_datetime','creation_user','downtime_start','planner','work_class','work_category','work_priority','requestor','owning_access_group','first_name','last_name','primary_phone','mobile_phone','home_phone','node_id','asset_id','status','int10_type','work_request_id','work_request_status','created_date','modified_date').order_by('-modified_date')
#         # queryset = WorkOrderActivityCompletion.objects.all().order_by('required_by_dt')
#         # queryset1 = WorkOrderActivityCompletion.objects.filter(record_by=userid).order_by('required_by_dt')
#         # queryset2 = WorkOrderActivityCompletion.objects.filter(record_by__isnull=True,status='BackLog').order_by('required_by_dt')
#         # queryset3 = WorkOrderActivityCompletion.objects.filter(status='New').order_by('required_by_dt')
#         # result_list = list(chain(queryset1,queryset2,queryset3))

#         # serializer_class = WorkOrderActivityCompletionPipeSerializer(
#         #     work_order_act_comp, many=True)

#         return Response(work_order_act_comp)

#     @action(methods=['POST'], detail=False)
#     def get_created_by(self, request, *args, **kwargs):

#         userid = self.request.data['userid']
#         print("userid ==== ",userid)
#         queryset = WorkOrderActivityCompletion.objects.filter(record_by=userid)

#         serializer = WorkOrderActivityCompletionSerializer(
#             queryset, many=True)
#         return Response(serializer.data)


class WorkOrderActivityCompletionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkOrderActivityCompletion.objects.all()
    serializer_class = WorkOrderActivityCompletionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'activityid', 'bo_status_cd', 'act_type_cd', 'service_class_cd', 'descr100','descrlong','field_1','field_2','status','owning_organization'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkOrderActivityCompletion.objects.all()

        # FROM APPLICATION/JSON THROUGH API
        if bool(self.request.data):
            print("enter bool()")
            if 'from_date' in self.request.data and 'to_date' in self.request.data:

                from_date = self.request.data.get('from_date', None)
                to_date = self.request.data.get('to_date', None)

                if from_date is not None and to_date is not None:
                    # print(WorkOrderActivityCompletion.objects.filter(submitted_datetime__range=(from_date,to_date)).query)
                    queryset = WorkOrderActivityCompletion.objects.filter(
                        submitted_datetime__range=(from_date, to_date))

        return queryset

    @action(methods=['POST'], detail=False)
    def extended_all(self, request, *args, **kwargs):

        from_date = self.request.data['from_date']
        to_date = self.request.data['to_date']

        # queryset = WorkOrderActivityCompletion.objects.all()
        queryset = WorkOrderActivityCompletion.objects.values_list('id','activityid','completiondatetime','bo_status_cd','user_id_1','act_type_cd','wo_id','act_dpos_flg','service_class_cd','requestor_id','required_by_dt','work_priority_flg','descr100','descrlong','w1_descr100_upr','held_for_parts_flg','anniversary_value','emergency_flg','act_num','planner_cd','total_priority','total_priority_src_flg','node_id_1','asset_id_1','percentage','seqno','participation_flg','cost_center_cd','percentage_2','act_resrc_reqmt_id','descrlong_1','resrc_src_flg','resrc_type_id','w1_quantity','unit_price','w1_duration','crew_shift_id','sched_duration','break_in_dttm','actvn_dttm','tmpl_act_id','maint_sched_id','maint_trigger_id','status','owning_organization','field_1','field_2','submitted_datetime','created_date','modified_date','asset_location_asset_list')

        # if from_date is not None and to_date is not None:
        #     queryset = WorkOrderActivityCompletion.objects.filter(
        #         submitted_datetime__range=(from_date, to_date)).values('id','activityid','completiondatetime','bo_status_cd','user_id_1','act_type_cd','wo_id','act_dpos_flg','service_class_cd','requestor_id','required_by_dt','work_priority_flg','descr100','descrlong','w1_descr100_upr','held_for_parts_flg','anniversary_value','emergency_flg','act_num','planner_cd','total_priority','total_priority_src_flg','node_id_1','asset_id_1','percentage','seqno','participation_flg','cost_center_cd','percentage_2','act_resrc_reqmt_id','descrlong_1','resrc_src_flg','resrc_type_id','w1_quantity','unit_price','w1_duration','crew_shift_id','sched_duration','break_in_dttm','actvn_dttm','tmpl_act_id','maint_sched_id','maint_trigger_id','status','owning_organization','field_1','field_2','submitted_datetime','created_date','modified_date','asset_location_asset_list')

        serializer = WorkOrderActivityCompletionExtendedSerializer(
            queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def extended(self, request, *args, **kwargs):
        work_order_activity = self.get_object()

        serializer = WorkOrderActivityCompletionExtendedSerializer(
            work_order_activity)
        return Response(serializer.data)

    # @action(methods=['GET'], detail=False)
    @action(methods=['POST'], detail=False)
    def asc_ordered_list(self, request, *args, **kwargs):
        
        userid = self.request.data['userid']
        user_details = CustomUser.objects.filter(id=userid).values('employee_id')

        print(user_details)
        emp_id = ''

        for i in user_details:
            emp_id = i['employee_id']

        work_act_emp = WorkActivityEmployee.objects.filter(employee_id=emp_id).values('work_order_activity_completion_id').order_by('created_date')
        print("work_act_emp",work_act_emp)

        work_order_act_comp = []
        no = 0
        for j in work_act_emp:
            print("work_act_emp------------------",j['work_order_activity_completion_id'])
            print("no -- ",no)
            # if no <= 1:
            woac_det = WorkOrderActivityCompletion.objects.filter(id=j['work_order_activity_completion_id']).values('id','activityid','completiondatetime','bo_status_cd','user_id_1','act_type_cd','wo_id','act_dpos_flg','service_class_cd','requestor_id','required_by_dt','work_priority_flg','descr100','descrlong','w1_descr100_upr','held_for_parts_flg','anniversary_value','emergency_flg','act_num','planner_cd','total_priority','total_priority_src_flg','node_id_1','asset_id_1','percentage','seqno','participation_flg','cost_center_cd','percentage_2','act_resrc_reqmt_id','descrlong_1','resrc_src_flg','resrc_type_id','w1_quantity','unit_price','w1_duration','crew_shift_id','sched_duration','break_in_dttm','actvn_dttm','tmpl_act_id','maint_sched_id','maint_sched_id','status','owning_organization','field_1','field_2','submitted_datetime','created_date','modified_date','asset_location_asset_list')
            # woac_det = WorkOrderActivityCompletion.objects.get(id=j['work_order_activity_completion_id']).values_list()
            work_order_act_comp.insert(no,woac_det[0])
        
            # print(woac_det)
            print(woac_det[0])

            no = no + 1

        return Response(work_order_act_comp)

    @action(methods=['POST'], detail=False)
    def get_created_by(self, request, *args, **kwargs):

        userid = self.request.data['userid']
        print("userid ==== ",userid)
        queryset = WorkOrderActivityCompletion.objects.filter(record_by=userid)

        serializer = WorkOrderActivityCompletionSerializer(
            queryset, many=True)
        return Response(serializer.data)


# end copied from dev api


class ServiceHistoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ServiceHistory.objects.all()
    serializer_class = ServiceHistorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'service_hist_type', 'service_hist_desc', 'service_hist_bo', 'category', 'service_hist_subclass'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = ServiceHistory.objects.all()

        return queryset


class ServiceHistoryQuestionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ServiceHistoryQuestion.objects.all()
    serializer_class = ServiceHistoryQuestionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'question_seq', 'question_cd', 'question_desc', 'service_history_id'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = ServiceHistoryQuestion.objects.all()

        return queryset

    @action(methods=['POST'], detail=False)
    def get_service_history_qna(self, request):

        data = json.loads(request.body)
        print("data",data)
        service_history_id = data['service_history_id']
        queryset_question = ServiceHistoryQuestion.objects.filter(service_history_id=service_history_id).values(
            'id', 'question_seq', 'question_cd', 'question_desc', 'service_history_id')

        data = []
        for qs_qs in queryset_question:
            valid_value = []
            queryset_answer = ServiceHistoryQuestionValidValue.objects.filter(service_history_question_id=qs_qs['id']).values(
                'id', 'answer_seq', 'answer_cd', 'answer_text', 'answer_desc', 'point_value', 'style', 'service_history_question_id')

            # for qs_aw in queryset_answer:

            no = 0
            for qs_ans in queryset_answer:
                print("qs_ans",qs_ans)
                print("qs_ans",qs_ans['style'])
                if qs_ans['style'] == 'W1RB':
                    valid_value.insert(no,qs_ans)
                    no += 1


            dictionary = {
                'question': qs_qs,
                'answer': valid_value
            }
            data.append(dictionary)
        return Response(data)


class ServiceHistoryQuestionValidValueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ServiceHistoryQuestionValidValue.objects.all()
    serializer_class = ServiceHistoryQuestionValidValueSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = ServiceHistoryQuestionValidValue.objects.all()

        return queryset


class PlannerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'planner',
        'status',
        'user_id'
    ]
    search_fields = ['$planner', '$user_id']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Planner.objects.all()

        return queryset


class MaintenanceManagerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = MaintenanceManager.objects.all()
    serializer_class = MaintenanceManagerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'maintenance_manager',
        'status',
        'user_id'
    ]
    search_fields = ['$maintenance_manager', '$user_id']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = MaintenanceManager.objects.all()

        return queryset


class MainOperationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = MainOperation.objects.all()
    serializer_class = MainOperationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = MainOperation.objects.all()

        return queryset


class FunctionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Function.objects.all()

        return queryset


class LocationTypeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = LocationType.objects.all()

        return queryset


class SubFunctionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = SubFunction.objects.all()
    serializer_class = SubFunctionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = SubFunction.objects.all()

        return queryset


class CostCenterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = CostCenter.objects.all()

        return queryset


class OperationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Operation.objects.all()

        return queryset


class WorkActivityEmployeeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkActivityEmployee.objects.all()
    serializer_class = WorkActivityEmployeeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkActivityEmployee.objects.all()

        return queryset

    @action(methods=['POST'], detail=False)
    def get_dashboard_status_statistic(self, request):

        data = json.loads(request.body)

        employee_id = data['employee_id']
        now = datetime.now()

        queryset_overall = WorkActivityEmployee.objects.filter(employee_id=employee_id).values(status=F(
            'work_order_activity_completion_id__status')).annotate(total_status=Count('work_order_activity_completion_id__status'))
        queryset_today = WorkActivityEmployee.objects.filter(created_date__date=now.strftime("%Y-%m-%d"), employee_id=employee_id).values(
            status=F('work_order_activity_completion_id__status')).annotate(total_status=Count('work_order_activity_completion_id__status'))

        data = {
            'queryset_overall': queryset_overall,
            'queryset_today': queryset_today
        }

        return Response(data)


class WorkOrderActivityCompletionAssetLocationAssetListInboundViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = WorkOrderActivityCompletionAssetLocationAssetListInbound.objects.all()
    serializer_class = WorkOrderActivityCompletionAssetLocationAssetListInboundSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = WorkOrderActivityCompletionAssetLocationAssetListInbound.objects.all()

        return queryset


class AssetLocationAssetListServiceHistoriesInboundViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetLocationAssetListServiceHistoriesInbound.objects.all()
    serializer_class = AssetLocationAssetListServiceHistoriesInboundSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = AssetLocationAssetListServiceHistoriesInbound.objects.all()

        return queryset
