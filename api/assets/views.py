
import json
import xlsxwriter
import io

from django.shortcuts import render
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from datetime import datetime
# from datetime import datetime
import pytz


from .models import (
    Asset,
    AssetRegistration,AssetRegistrationBk,
    AssetGroup,
    AssetType,
    Rfid,
    AssetBadgeFormat,
    AssetAttribute,
    AssetAttributeColumn,
    AssetLocation,
    AssetMeasurementType,
    AssetLocationSync,
    AssetAttributeField,
    AssetMeasurementTypeInbound,
    AssetAttributeInbound,
    AssetServiceHistory,
    AssetMaintenanceSpec,
    AssetAttributeReference,
    AssetAttributePredefine
)

from .serializers import (
    AssetSerializer,
    AssetRegistrationSerializer,AssetRegistrationBkSerializer,
    AssetGroupSerializer,
    AssetTypeSerializer,
    RfidSerializer,
    AssetBadgeFormatSerializer,
    AssetAttributeSerializer,
    AssetAttributeColumnSerializer,
    AssetLocationSerializer,
    AssetMeasurementTypeSerializer,
    AssetExtendedSerializer,
    AssetLocationSyncSerializer,
    AssetAttributeFieldSerializer,
    AssetMeasurementTypeInboundSerializer,
    AssetAttributeInboundSerializer,
    AssetServiceHistorySerializer,
    AssetMaintenanceSpecSerializer,
    AssetAttributeReferenceSerializer,
    AssetAttributePredefineSerializer
)

class AssetViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = []
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_id',
        'badge_no',
        'node_id',
        'hex_code',
        'attached_to_asset_id'
    ]

    @action(methods=['POST'], detail=False)
    def patch_asset(self, request, *args, **kwargs):
        asset_request_ = json.loads(request.body)
        asset_hex_code_ = asset_request_['hex_code']
        asset_badge_no_ = asset_request_['badge_no']

        asset_ = Asset.objects.filter(
            badge_no=asset_badge_no_
        ).first()

        asset_.hex_code = asset_hex_code_
        asset_.save()

        print('asset =')
        print(asset_)

        serializer = AssetSerializer(asset_)
        return Response(serializer.data)  
        # rejected_list_serializer = AssetRegistrationSerializer(rejected_list_asset_list, many=True)
        # return Response(rejected_list_serializer.data) 

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    def get_queryset(self):
        queryset = Asset.objects.all()

        # FROM APPLICATION/JSON THROUGH API
        if bool(self.request.data):
            print("enter bool()")
            if 'from_date' in self.request.data and 'to_date' in self.request.data and 'transaction_type' in self.request.data:

                from_date = self.request.data.get('from_date', None)
                to_date = self.request.data.get('to_date', None)
                transaction_type_req = self.request.data.get(
                    'transaction_type', None)

                if from_date is not None and to_date is not None and transaction_type_req is not None:
                    print(Asset.objects.filter(submitted_datetime__range=(
                        from_date, to_date), transaction_type=(transaction_type_req)).query)
                    queryset = Asset.objects.filter(submitted_datetime__range=(
                        from_date, to_date), transaction_type=(transaction_type_req))

        return queryset

    @action(methods=['POST'], detail=False)
    def extended_all(self, request, *args, **kwargs):
        from_date = self.request.data['from_date']
        to_date = self.request.data['to_date']
        transaction_type = self.request.data['transaction_type']

        # Note
        # If transaction_type = ADD, filter by registered_datetime
        # If transaction_type = UPDATE, filter by submitted_datetime

        if from_date is not None and to_date is not None and transaction_type is not None:
            if transaction_type == 'ADD':
                queryset = Asset.objects.filter(registered_datetime__range=(
                    from_date, to_date)).filter(transaction_type=transaction_type)
            elif transaction_type == 'UPDATE':
                queryset = Asset.objects.filter(submitted_datetime__range=(
                    from_date, to_date)).filter(transaction_type=transaction_type)

        serializer = AssetExtendedSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def extended(self, request, *args, **kwargs):
        asset_ = self.get_object()

        serializer = AssetExtendedSerializer(asset_)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def activate(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.is_active = True
        asset.save()

        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    
    @action(methods=['GET'], detail=True)
    def deactivate(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.is_active = False
        asset.save()

        serializer = AssetSerializer(asset)
        return Response(serializer.data)


    @action(methods=['GET'], detail=True)
    def warranty_end(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.is_warranty = False
        asset.save()

        serializer = AssetSerializer(asset)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=True)
    def approve(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.approval_status = 'AP'
        asset.approval_by = self.request.user
        asset.approval_at = datetime.now()
        asset.save()

        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def reject(self, request, *args, **kwargs):
        asset = self.get_object()
        asset.approval_status = 'RJ'
        asset.approval_by = self.request.user
        asset.approval_at = datetime.now()
        asset.save()

        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    @action(methods=['POST', 'GET'], detail=False)
    def exportExcel(self, request, *args, **kwargs):
        temp = []
        for i in request.data["selected_id"]:
            temp.append(AssetRegistration.objects.all().filter(id=i).values()[0])

        temp_list = [i for i in temp]


        output = io.BytesIO()
        file_name = 'RegisteredAsset.xlsx'
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('registered_asset')
        
        # get header 
        header = [*temp_list[0]]
        print(header)

        first_row = 0
        for h in header:
            col = header.index(h)
            worksheet.write(first_row, col, h)

        row = 1
        for i in temp_list:
            for _key, _value in i.items():
                col = header.index(_key)
                worksheet.write(row, col, str(_value))
            row+=1

        workbook.close()
        output.seek(0)
         
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="' + file_name +'"'
        return response

    @action(methods=['GET'], detail=False)
    def udpate_effective_datetime(self, request, *args, **kwargs):
        
        print("ttettetettete")
        queryset = Asset.objects.all()[:15]


        # for i in queryset:

        #     print("effective_datetime >> ",i.effective_datetime)

        #     # eff_datetime = format_datetime(i.effective_datetime)
        #     # print("eff_datetime",eff_datetime)
        #     # 2016-11-15 00:00:00+00:00
        #     # "%Y-%m-%d-%H.%M.%S"

        #     timezone = pytz.timezone('Asia/Kuala_Lumpur')
        #     # datetime_data = timestamp.strftime((i.effective_datetime, '%Y-%m-%d %H:%M:%S')
        #     # print("datetime_data",datetime_data)

        #     datetime_timezone = timezone.localize(datetime_data)

        #     datetime.datetime(i.effective_datetime, tzinfo=<UTC>)
        #     print("effective_datetime1111 >>> ",effective_datetime)
            
        #     effective_datetime = datetime_timezone.astimezone(pytz.utc)

        #     print("effective_datetime2222 >>> ",effective_datetime)

        
        # asset.approval_by = self.request.user
        # asset.approval_at = datetime.now()
        # asset.save()

        # serializer = AssetSerializer(asset)
        # return Response(serializer.data)


class AssetGroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'category',
        'created_at'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetGroup.objects.all()

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

class AssetTypeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_bussiness_object','asset_type_code','asset_type_description','status','assessment_class'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetType.objects.all()

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

class RfidViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Rfid.objects.all()
    serializer_class = RfidSerializer
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
        queryset = Rfid.objects.all()

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

class AssetRegistrationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetRegistration.objects.all()
    serializer_class = AssetRegistrationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_id',
        'badge_no',
        'node_id',
        'hex_code',
        'created_at'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetRegistration.objects.all()

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


    @action(methods=['GET'], detail=False)
    def new_register_list(self, request, *args, **kwargs):

        asset_list = AssetRegistration.objects.filter(Q(status='CO') | Q(status='IC'))

        serializer = AssetRegistrationSerializer(asset_list, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def processed_list(self, request, *args, **kwargs):

        asset_list = AssetRegistration.objects.filter(status='PR')

        serializer = AssetRegistrationSerializer(asset_list, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def new_processed_list(self, request, *args, **kwargs):

        asset_list = AssetRegistration.objects.filter(status='NP')

        serializer = AssetRegistrationSerializer(asset_list, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def approved_list(self, request, *args, **kwargs):

        asset_list = AssetRegistration.objects.filter(status='AP')

        serializer = AssetRegistrationSerializer(asset_list, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def rejected_list(self, request, *args, **kwargs):

        rejected_list_asset_list = AssetRegistration.objects.filter(status='RJ')
        print('asset_list = ')
        print(rejected_list_asset_list)
        rejected_list_serializer = AssetRegistrationSerializer(rejected_list_asset_list, many=True)
        return Response(rejected_list_serializer.data)


    @action(methods=['GET'], detail=False)
    def Remove_all_record(self, request, *args, **kwargs):

        AssetRegistration.objects.all().delete()

        print('asset_list = ')
        # print(rejected_list_asset_list)
        # rejected_list_serializer = AssetRegistrationSerializer(rejected_list_asset_list, many=True)
        # return Response(rejected_list_serializer.data)
    
    @action(methods=['POST'], detail=False)
    def patch_asset(self, request, *args, **kwargs):
        asset_request_ = json.loads(request.body)
        asset_hex_code_ = asset_request_['hex_code']
        asset_badge_no_ = asset_request_['badge_no']

        asset_ = AssetRegistration.objects.filter(
            badge_no=asset_badge_no_
        ).first()

        asset_.hex_code = asset_hex_code_
        asset_.save()

        print('asset =')
        print(asset_)

        serializer = AssetRegistrationSerializer(asset_)
        return Response(serializer.data)  
        # rejected_list_serializer = AssetRegistrationSerializer(rejected_list_asset_list, many=True)
        # return Response(rejected_list_serializer.data) 


class AssetRegistrationBkViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetRegistrationBk.objects.all()
    serializer_class = AssetRegistrationBkSerializer
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
        queryset = AssetRegistrationBk.objects.all()
        return queryset


class AssetBadgeFormatViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetBadgeFormat.objects.all()
    serializer_class = AssetBadgeFormatSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_primary_category',
        'status'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetBadgeFormat.objects.all()

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

class AssetAttributeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetAttribute.objects.all()
    serializer_class = AssetAttributeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetAttribute.objects.all()

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

class AssetAttributeColumnViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetAttributeColumn.objects.all()
    serializer_class = AssetAttributeColumnSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_type_id'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetAttributeColumn.objects.all()

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

class AssetLocationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetLocation.objects.all()
    serializer_class = AssetLocationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
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
        queryset = AssetLocation.objects.all()

        # FROM APPLICATION/JSON THROUGH API
        if bool(self.request.data):
            print("enter bool()")
            if 'from_date' in self.request.data and 'to_date' in self.request.data:

                from_date = self.request.data.get('from_date', None)
                to_date = self.request.data.get('to_date', None)

                if from_date is not None and to_date is not None:
                    # print(AssetLocation.objects.filter(submitted_datetime__range=(from_date,to_date)).query)
                    queryset = AssetLocation.objects.filter(
                        submitted_datetime__range=(from_date, to_date))

        return queryset

    @action(methods=['POST'], detail=False)
    def extended_all(self, request, *args, **kwargs):

        from_date = self.request.data['from_date']
        to_date = self.request.data['to_date']

        if from_date is not None and to_date is not None:
            queryset = AssetLocation.objects.filter(
                submitted_datetime__range=(from_date, to_date))

        serializer = AssetLocationSerializer(queryset, many=True)
        return Response(serializer.data)

class AssetMeasurementTypeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetMeasurementType.objects.all()
    serializer_class = AssetMeasurementTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = AssetMeasurementType.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()

        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company

            if company.company_type == 'AD':
                queryset = AssetMeasurementType.objects.all()
            else:
                queryset = AssetMeasurementType.objects.filter(company=company.id)
        """
        return queryset

class AssetLocationSyncViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetLocationSync.objects.all()
    serializer_class = AssetLocationSyncSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'node_id','description'
    ]
    search_fields = ['$node_id', '$description']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetLocationSync.objects.all()

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

    @action(methods=['GET'], detail=False)
    def get_asset_location(self, request, *args, **kwargs):

        query = AssetLocationSync.objects.all()[:100]  
        print(query)
        serializer = AssetLocationSyncSerializer(query, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def no_duplicate_list(self, request, *args, **kwargs):

        # asset_list = AssetRegistration.objects.filter(status='AP')

        # serializer = AssetRegistrationSerializer(asset_list, many=True)
        # return Response(serializer.data)

        # asset_list = AssetRegistration.objects.filter(status='PR')
        queryset = AssetLocationSync.objects.values_list().distinct()

        print(queryset)

        # for i in queryset:
        #     print(i)


        serializer = AssetLocationSyncSerializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)

class AssetAttributeFieldViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetAttributeField.objects.all()
    serializer_class = AssetAttributeFieldSerializer
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
        queryset = AssetAttributeField.objects.all()

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

class AssetMeasurementTypeInboundViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = AssetMeasurementTypeInbound.objects.all()
    serializer_class = AssetMeasurementTypeInboundSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'measurement_type','action_type','description','measurement_identifie','asset_id'
    ]
    search_fields = ['$node_id', '$description']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetMeasurementTypeInbound.objects.all()

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
 
class AssetAttributeInboundViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = AssetAttributeInbound.objects.all()
    serializer_class = AssetAttributeInboundSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'characteristic_type','adhoc_value','characteristic_value','action_type','asset_id'
    ]
    # search_fields = ['$node_id', '$description']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetAttributeInbound.objects.all()

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

class AssetServiceHistoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetServiceHistory.objects.all()
    serializer_class = AssetServiceHistorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'asset_service_history'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssetServiceHistory.objects.all()

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

class AssetMaintenanceSpecViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetMaintenanceSpec.objects.all()
    serializer_class = AssetMaintenanceSpecSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'maintenance_spec_cd','asset_type_cd'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    def get_queryset(self):
        queryset = AssetMaintenanceSpec.objects.all()

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

class AssetAttributeReferenceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetAttributeReference.objects.all()
    serializer_class = AssetAttributeReferenceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'char_type_cd','attribute_field_name'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    def get_queryset(self):
        queryset = AssetAttributeReference.objects.all()

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

class AssetAttributePredefineViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssetAttributePredefine.objects.all()
    serializer_class = AssetAttributePredefineSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'attribute_field_name','characteristic_value'
    ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    def get_queryset(self):
        queryset = AssetAttributePredefine.objects.all()

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
