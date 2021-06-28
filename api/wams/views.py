from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.core.files.storage import default_storage
from django.utils.timezone import make_aware

from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.conf import settings

import json
import base64

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime

from wams.services.int01_employee import get_employee
from wams.services.int02_workorderactivity import get_workorderactivity
from wams.services.int04_assetsyncoutbound import get_assetsyncoutbound
from wams.services.int07_servicehistorytype import get_servicehistorytype
from wams.services.int08_failureprofile import get_failureprofile
from wams.services.int09_measurementtype import get_measurementtype
from wams.services.int10_inboundworkrequest import get_inboundworkrequest
from wams.services.int11_planner import get_planner
from wams.services.int15_asset import get_asset
from wams.services.int16_workrequeststatusupdate import get_workrequeststatusupdate
from wams.services.int18_assetlocation import get_assetlocation
from wams.services.int19_maintenancemanager import get_maintenancemanager
from wams.services.int99_activedirectory import get_active_directory

from .models import (
    Wams
)

from .serializers import (
    WamsSerializer
)

class WamsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Wams.objects.all()
    serializer_class = WamsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        print('Version baru')
        queryset = Wams.objects.all()
        return queryset

    @action(methods=['POST'], detail=False)
    def services(self, request, *args, **kwargs):

        call_json = json.loads(request.body)
        request_service_name = call_json['service_name']

        if request_service_name == 'getEmployee':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_employee(from_date, to_date)
            # for single result only
            # json_response = {
            #     'result': { k.replace('ouaf:', ''): v for k, v in middleware_call.items() }
            # }
            json_response = middleware_call

        elif request_service_name == 'getWorkOrderActivity':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_workorderactivity(from_date, to_date)
            # for multiple results only
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getAssetSyncOutbound':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_assetsyncoutbound(from_date, to_date)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getServiceHistoryType':
            middleware_call = get_servicehistorytype()
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getFailureProfile':
            middleware_call = get_failureprofile()
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getMeasurementType':
            middleware_call = get_measurementtype()
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getInboundWorkRequest':
            request_int10_type = call_json['int10_type'] if call_json['int10_type'] else None

            # CREATE
            if request_int10_type == 'create':

                description = call_json['description'] if call_json['description'] else None
                long_description = call_json['long_description'] if call_json['long_description'] else None
                required_by_date = call_json['required_by_date'] if call_json['required_by_date'] else None
                approval_profile = call_json['approval_profile'] if call_json['approval_profile'] else None
                bo = call_json['bo'] if call_json['bo'] else None
                creation_datetime = call_json['creation_datetime'] if call_json['creation_datetime'] else None
                creation_user = call_json['creation_user'] if call_json['creation_user'] else None
                downtime_start = call_json['downtime_start'] if call_json['downtime_start'] else None
                planner = call_json['planner'] if call_json['planner'] else None
                work_class = call_json['work_class'] if call_json['work_class'] else None
                work_category = call_json['work_category'] if call_json['work_category'] else None
                work_priority = call_json['work_priority'] if call_json['work_priority'] else None
                requestor = call_json['requestor'] if call_json['requestor'] else None
                owning_access_group = call_json['owning_access_group'] if call_json['owning_access_group'] else None
                first_name = call_json['first_name'] if call_json['first_name'] else None
                last_name = call_json['last_name'] if call_json['last_name'] else None
                primary_phone = call_json['primary_phone'] if call_json['primary_phone'] else None
                mobile_phone = call_json['mobile_phone'] if call_json['mobile_phone'] else None
                home_phone = call_json['home_phone'] if call_json['home_phone'] else None
                node_id = call_json['node_id'] if call_json['node_id'] else None
                asset_id = call_json['asset_id'] if call_json['asset_id'] else None

                data = {
                    'description': description,
                    'long_description': long_description,
                    'required_by_date': required_by_date,
                    'approval_profile': approval_profile,
                    'bo': bo,
                    'creation_datetime': creation_datetime,
                    'creation_user': creation_user,
                    'downtime_start': downtime_start,
                    'planner': planner,
                    'work_class': work_class,
                    'work_category': work_category,
                    'work_priority': work_priority,
                    'requestor': requestor,
                    'owning_access_group': owning_access_group,
                    'first_name': first_name,
                    'last_name': last_name,
                    'primary_phone': primary_phone,
                    'mobile_phone': mobile_phone,
                    'home_phone': home_phone,
                    'node_id': node_id,
                    'asset_id': asset_id
                }

            # UPDATE
            elif request_int10_type == 'update':
            
                work_request_id = call_json['work_request_id'] if call_json['work_request_id'] else None
                approval_profile = call_json['approval_profile'] if call_json['approval_profile'] else None
                work_request_status = call_json['work_request_status'] if call_json['work_request_status'] else None

                data = {
                    'work_request_id': work_request_id,
                    'approval_profile': approval_profile,
                    'work_request_status': work_request_status
                }

            middleware_call = get_inboundworkrequest(request_int10_type, data)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getPlanner':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_planner(from_date, to_date)

            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getAsset':
            badge_number = call_json['badge_number'] if call_json['badge_number'] is not None else None

            middleware_call = get_asset(badge_number)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getWorkRequestStatusUpdate':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_workrequeststatusupdate(from_date, to_date)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getAssetLocation':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_assetlocation(from_date, to_date)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getMaintenanceManager':
            from_date = call_json['from_date'] if call_json['from_date'] is not None else None
            to_date = call_json['to_date'] if call_json['to_date'] is not None else None

            middleware_call = get_maintenancemanager(from_date, to_date)
            
            # middleware_list = []
            # for item in middleware_call:
            #     new_json = {}
            #     for key in item:
            #         new_key = key.replace('ouaf:', '')
            #         new_json[new_key] = item[key]
            #     middleware_list.append(new_json)
            
            # json_response = {
            #     'result': middleware_list
            # }
            json_response = middleware_call

        elif request_service_name == 'getActiveDirectory':
            username = call_json['username'] if call_json['username'] is not None else None
            password = call_json['password'] if call_json['password'] is not None else None

            middleware_call = get_active_directory(username, password)

            json_response = middleware_call


        return JsonResponse(json_response)
