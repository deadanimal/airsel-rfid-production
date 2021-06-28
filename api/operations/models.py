# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid, datetime

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

from simple_history.models import HistoricalRecords

from assets.models import (
    Asset
)
from medias.models import (
    Media
)
from users.models import (
    CustomUser
)
from employee.models import (
    Employee
)

from core.helpers import PathAndRename

class OwningOrganization(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=255, default='NA')
    detail_description = models.TextField(default='NA')

    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return self.name

class Bo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=255, default='NA')
    status = models.BooleanField(default=True)

    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return self.name

class Maintenance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_num = models.CharField(max_length=100, default='NA')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.serial_num

class IssueType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class WorkOrder(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wams_id = models.CharField(max_length=100, default='NA')
    work_order_description = models.CharField(max_length=100, default='NA')
    planner_cd = models.CharField(max_length=100, default='NA')
    planner_name = models.CharField(max_length=100, default='NA')
    work_order_no = models.CharField(max_length=100, default='NA')
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class meta:
        ordering = ['planner_name']
    
    def __str__(self):
        #return "{} {} {}".format(self.name, self.activity, self.created_at)
        return self.wams_id

class WorkActivity(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bo_status = models.CharField(max_length=100, default='NA')
    required_by_date = models.DateField(default=datetime.date.today)
    parent_location = models.CharField(max_length=100, default='NA')
    activity_id = models.CharField(max_length=50, default='NA')
    work_class = models.CharField(max_length=100, default='NA')
    work_category = models.CharField(max_length=100, default='NA')
    description = models.TextField(default='NA')
    completion_date_time = models.DateTimeField(blank=True, null=True)
    node_id = models.CharField(max_length=12, default='NA')
    asset_id = models.CharField(max_length=12, default='NA')
    asset_type = models.CharField(max_length=50, default='NA')
    badge_number = models.CharField(max_length=50, default='NA')
    serial_number = models.CharField(max_length=50, default='NA')
    detailed_description = models.TextField(default='NA')
    participation = models.CharField(max_length=50, default='NA')
    # service history type: downtime
    service_history_type_dt = models.CharField(max_length=50, default='NA', blank=True)
    effective_date_time_dt = models.DateTimeField(blank=True, null=True)
    comments_dt = models.TextField(default='NA', blank=True)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    downtime_reason = models.CharField(max_length=50, default='NA')
    # service history type: failure
    service_history_type_f = models.CharField(max_length=50, default='NA', blank=True)
    effective_date_time_f = models.DateTimeField(blank=True, null=True)
    comments_f = models.TextField(default='NA', blank=True)
    failure_type = models.CharField(max_length=50, default='NA', blank=True)
    failure_mode = models.CharField(max_length=50, default='NA', blank=True)
    failure_repair = models.CharField(max_length=50, default='NA', blank=True)
    failure_component = models.CharField(max_length=50, default='NA', blank=True)
    failure_root_cause = models.TextField(default='NA', blank=True)
    # service history type: preventive maintenance
    service_history_type_pm = models.CharField(max_length=50, default='NA')
    effective_date_time_pm = models.DateTimeField(blank=True, null=True)
    comments_pm = models.TextField(default='NA')
    answer_1 = models.CharField(max_length=100, blank=True)
    answer_2 = models.CharField(max_length=100, blank=True)
    answer_3 = models.CharField(max_length=100, blank=True)

    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['required_by_date']
    
    def __str__(self):
        #return "{} {} {}".format(self.name, self.activity, self.created_at)
        return self.activity_id

class WorkActivityTeam(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_activity = models.ForeignKey(
        WorkActivity,
        on_delete=models.CASCADE,
        null=True,
        related_name='work_activity_team_wa'
    )
    teammate = models.ManyToManyField(
        CustomUser,
        related_name='work_activity_teammate',
        limit_choices_to={
            'user_type': 'TC'
        }
    )
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return "{}".format(self.work_activity)

class WorkClass(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=255, default='NA')

    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return self.name

class WorkCategory(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_category = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=255, blank=True)
    # detail_description = models.TextField(default='NA')
    # status = models.BooleanField(default=True)

    # record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    # modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name

class WorkRequest(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # description = models.CharField(max_length=255, default='NA')
    # long_description = models.TextField(default='NA')
    # required_by_date = models.DateField(default=datetime.date.today)
    # bo_status = models.CharField(max_length=100, default='NA')
    # creation_date_time = models.DateTimeField(auto_now_add=True)
    # creation_user = models.CharField(max_length=100, default='NA')
    # down_time_start = models.DateTimeField(blank=True, null=True)
    # planner = models.CharField(max_length=100, default='NA')
    # work_class = models.CharField(max_length=100, default='NA')
    # work_category = models.CharField(max_length=100, default='NA')
    # work_priority = models.CharField(max_length=10, default='01')
    # requestor = models.CharField(max_length=100, default='NA')
    # owning_access_group = models.CharField(max_length=100, default='NA')
    # first_name = models.CharField(max_length=100, default='NA', blank=True)
    # last_name = models.CharField(max_length=100, default='NA', blank=True)
    # primary_phone = models.CharField(max_length=20, default='NA', blank=True)
    # mobile_phone = models.CharField(max_length=20, default='NA', blank=True)
    # home_phone = models.CharField(max_length=20, default='NA', blank=True)
    # node_id = models.CharField(max_length=50, default='NA')
    # asset_id = models.CharField(max_length=50, default='NA')
    # attachment = models.ForeignKey(
    #     Media,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name='work_request_attachment'
    # )

    # record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True)
    # record_date = models.DateTimeField(auto_now_add=True)
    # modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True)
    # modified_date = models.DateTimeField(auto_now=True)

    # class meta:
    #     ordering = ['-record_date']
    
    # def __str__(self):
    #     return self.description

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=100, blank=True)
    long_description = models.CharField(max_length=250, blank=True)
    required_by_date = models.CharField(max_length=100, blank=True)
    approval_profile = models.CharField(max_length=100, blank=True)
    bo = models.CharField(max_length=100, blank=True)
    creation_datetime = models.CharField(max_length=100, blank=True)
    creation_user = models.CharField(max_length=100, blank=True)
    downtime_start = models.CharField(max_length=100, blank=True)
    planner = models.CharField(max_length=100, blank=True)
    work_class = models.CharField(max_length=100, blank=True)
    work_category = models.CharField(max_length=100, blank=True)
    work_priority = models.CharField(max_length=100, blank=True)
    requestor = models.CharField(max_length=100, blank=True)
    owning_access_group = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    primary_phone = models.CharField(max_length=100, blank=True)
    mobile_phone = models.CharField(max_length=100, blank=True)
    home_phone = models.CharField(max_length=100, blank=True)
    node_id = models.CharField(max_length=12, blank=True)
    asset_id = models.CharField(max_length=12, blank=True)
    status = models.CharField(max_length=100, blank=True)
    int10_type = models.CharField(max_length=100, blank=True)
    work_request_id = models.CharField(max_length=100, blank=True)
    work_request_status = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_date = models.DateTimeField(auto_now=True)

    # new filed added for user id
    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True,blank=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True,blank=True)


    class meta:
        ordering = ['-created_date']

class WorkRequestStatus(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_request_id = models.CharField(max_length=50, blank=True,null=True)#models.ForeignKey(WorkRequest, on_delete=models.CASCADE, related_name='work_request_status_work_request_id', null=True)
    status = models.CharField(max_length=50, blank=True)
    
    # record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='work_request_status_record_by', null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    # modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='work_request_status_modified_by', null=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return self.status

class MeasurementType(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measurement_identifier = models.CharField(max_length=100, default='NA')
    measurement_type = models.CharField(max_length=100, default='NA')
    description = models.CharField(max_length=255, default='NA')
    
    record_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']

    def __str__(self):
        return self.measurement_identifier

class OperationalReading(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(max_length=12, blank=True)
    badge_number = models.CharField(max_length=100, blank=True)
    current_value = models.CharField(max_length=100, blank=True)
    measurent_identifier = models.CharField(max_length=100, blank=True)
    measurent_type = models.CharField(max_length=100, blank=True)
    initial_value_flag = models.CharField(max_length=100, blank=True)
    owning_organization = models.CharField(max_length=100, blank=True)
    reading_datetime = models.DateTimeField(null=True,blank=True)

    submitted_datetime = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # new filed added for user id
    record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True,blank=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True,blank=True)


    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.asset_id

#### below is the code copied from dev api
class QuestionsValidValue(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    seq_valid = models.CharField(max_length=100, blank=True)
    code_valid = models.CharField(max_length=100, blank=True)
    short_text_valid = models.CharField(max_length=100, blank=True)
    text_valid = models.CharField(max_length=250, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s'%(self.seq_valid, self.code_valid))

class ServiceHistoriesQuestions(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    seq = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=100, blank=True)
    short_text = models.CharField(max_length=100, blank=True)
    text = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    valid_value = models.ManyToManyField(QuestionsValidValue, blank=True)
    respone = models.CharField(max_length=100, blank=True)
    response_check_box = models.CharField(max_length=100, blank=True)
    response_radio = models.CharField(max_length=100,blank=True)
    responseDate = models.DateField(null=True)
    response_datetime = models.DateTimeField(auto_now=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s'%(self.seq, self.code))

class AssetLocationAssetListServiceHistories(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    service_history_type = models.CharField(max_length=100,blank=True)
    effective_datetime = models.DateTimeField(auto_now=True)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    comments = models.CharField(max_length=100, blank=True)
    failure_type = models.CharField(max_length=100, blank=True)
    failure_mode = models.CharField(max_length=100, blank=True)
    failure_repair = models.CharField(max_length=100, blank=True)
    failure_component = models.CharField(max_length=100, blank=True)
    failure_root_cause = models.CharField(max_length=100, blank=True)
    question = models.ManyToManyField(ServiceHistoriesQuestions, blank=True)
    svc_hist_type_req_fl = models.CharField(max_length=100, blank=True)
    downtime_reason = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    # def __str__(self):
    #     return self.service_history_type

class WorkOrderActivityCompletionAssetLocationAssetList(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    node_id = models.CharField(max_length=12, blank=True)
    asset_id = models.CharField(max_length=12, blank=True)
    participation = models.CharField(max_length=100, blank=True)
    service_histories = models.ManyToManyField(AssetLocationAssetListServiceHistories, blank=True)
    measurent_type = models.CharField(max_length=100, blank=True)
    reading_type = models.CharField(max_length=100, blank=True)
    current_value = models.CharField(max_length=100, blank=True)
    asset_description = models.CharField(max_length=100, blank=True)
    asset_type = models.CharField(max_length=100, blank=True)

    reading_datetime = models.DateTimeField(null=True,blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    # def __str__(self):
    #     return self.uuid

class WorkOrderActivityCompletion(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    activityid = models.CharField(max_length=100, blank=True)
    completiondatetime = models.DateTimeField(auto_now=True)
    asset_location_asset_list = models.ManyToManyField(WorkOrderActivityCompletionAssetLocationAssetList, blank=True)

    bo_status_cd = models.CharField(max_length=100, blank=True)
    user_id_1 = models.CharField(max_length=100, blank=True)
    act_type_cd = models.CharField(max_length=100, blank=True)
    wo_id = models.CharField(max_length=100, blank=True)
    act_dpos_flg = models.CharField(max_length=100, blank=True)
    service_class_cd = models.CharField(max_length=100, blank=True)
    requestor_id = models.CharField(max_length=100, blank=True)
    required_by_dt = models.CharField(max_length=100, blank=True)
    work_priority_flg = models.CharField(max_length=100, blank=True)
    descr100 = models.CharField(max_length=225, blank=True)
    descrlong = models.CharField(max_length=225, blank=True)
    w1_descr100_upr = models.CharField(max_length=225, blank=True)
    held_for_parts_flg = models.CharField(max_length=100, blank=True)
    anniversary_value = models.CharField(max_length=100, blank=True)
    emergency_flg = models.CharField(max_length=100, blank=True)
    act_num = models.CharField(max_length=100, blank=True)
    planner_cd = models.CharField(max_length=100, blank=True)
    total_priority = models.CharField(max_length=100, blank=True)
    total_priority_src_flg = models.CharField(max_length=100, blank=True)
    node_id_1 = models.CharField(max_length=12, blank=True)
    asset_id_1 = models.CharField(max_length=12, blank=True)
    percentage = models.CharField(max_length=100, blank=True)
    seqno = models.CharField(max_length=100, blank=True)
    participation_flg = models.CharField(max_length=100, blank=True)
    cost_center_cd = models.CharField(max_length=100, blank=True)
    percentage_2 = models.CharField(max_length=100, blank=True)
    act_resrc_reqmt_id = models.CharField(max_length=100, blank=True)
    descrlong_1 = models.CharField(max_length=100, blank=True)
    resrc_src_flg = models.CharField(max_length=100, blank=True)
    resrc_type_id = models.CharField(max_length=100, blank=True)
    w1_quantity = models.CharField(max_length=100, blank=True)
    unit_price = models.CharField(max_length=100, blank=True)
    w1_duration = models.CharField(max_length=100, blank=True)
    crew_shift_id = models.CharField(max_length=100, blank=True)
    sched_duration = models.CharField(max_length=100, blank=True)
    break_in_dttm = models.CharField(max_length=100, blank=True)
    actvn_dttm = models.CharField(max_length=100, blank=True)
    tmpl_act_id = models.CharField(max_length=100, blank=True)
    maint_sched_id = models.CharField(max_length=100, blank=True)
    maint_trigger_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    owning_organization = models.CharField(max_length=100, blank=True)

    field_1 = models.CharField(max_length=100, blank=True)
    field_2 = models.CharField(max_length=100, blank=True)

    submitted_datetime = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # new filed added for user id
    # record_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_record_by', null=True,blank=True)
    # modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', null=True,blank=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return ('%s %s'%(self.activityid, self.id))

#### above is the code copied from dev api

#### baru tambah
class ServiceHistory(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    service_hist_type = models.CharField(max_length=100, blank=True)
    service_hist_desc = models.CharField(max_length=225, blank=True)
    service_hist_bo = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    service_hist_subclass = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class ServiceHistoryQuestion(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    question_seq = models.CharField(max_length=100, blank=True)
    question_cd = models.CharField(max_length=225, blank=True)
    question_desc = models.CharField(max_length=225, blank=True)
    service_history_id = models.ForeignKey(ServiceHistory, on_delete=models.CASCADE, related_name='service_history_question_service_history_id', null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class ServiceHistoryQuestionValidValue(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    answer_seq = models.CharField(max_length=100, blank=True)
    answer_cd = models.CharField(max_length=225, blank=True)
    answer_desc = models.CharField(max_length=225, blank=True)
    answer_text = models.CharField(max_length=225, blank=True)
    point_value = models.CharField(max_length=100, blank=True)
    service_history_question_id = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    service_history_question_id = models.ForeignKey(ServiceHistoryQuestion, on_delete=models.CASCADE, related_name='service_history_question_valid_value_service_history_id', null=True)


    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class Planner(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    planner = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    user_id = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class MaintenanceManager(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    maintenance_manager = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    user_id = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class MainOperation(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    main_operation = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class Function(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    function = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class LocationType(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    location_type = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=250, blank=True)
    Bo = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class SubFunction(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    sub_function = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class CostCenter(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    costCenter = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=250, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class Operation(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    operation = models.CharField(max_length=100, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class WorkActivityEmployee(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    work_order_activity_completion_id = models.ForeignKey(WorkOrderActivityCompletion, on_delete=models.CASCADE, related_name='work_activity_emplyee_work_order_activity_completion_id', null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_work_activity_employee_id', null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

class WorkOrderActivityCompletionAssetLocationAssetListInbound(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    node_id = models.CharField(max_length=12, blank=True)
    activityid = models.CharField(max_length=100, blank=True)
    asset_id = models.CharField(max_length=12, blank=True)
    participation = models.CharField(max_length=100, blank=True)
    service_histories = models.ManyToManyField(AssetLocationAssetListServiceHistories, blank=True)
    measurent_type = models.CharField(max_length=100, blank=True)
    reading_type = models.CharField(max_length=100, blank=True)
    current_value = models.CharField(max_length=100, blank=True)
    asset_description = models.CharField(max_length=100, blank=True)
    asset_type = models.CharField(max_length=100, blank=True)
    reading_datetime = models.DateTimeField(null=True,blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.node_id

class AssetLocationAssetListServiceHistoriesInbound(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    activityid = models.CharField(max_length=100, blank=True)
    service_history_type = models.CharField(max_length=100,blank=True)
    effective_datetime = models.DateTimeField(auto_now=True)
    asset_id = models.CharField(max_length=12, blank=True)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    comments = models.CharField(max_length=100, blank=True)
    failure_type = models.CharField(max_length=100, blank=True)
    failure_mode = models.CharField(max_length=100, blank=True)
    failure_repair = models.CharField(max_length=100, blank=True)
    failure_component = models.CharField(max_length=100, blank=True)
    failure_root_cause = models.CharField(max_length=100, blank=True)
    question = models.ManyToManyField(ServiceHistoriesQuestions, blank=True)
    svc_hist_type_req_fl = models.CharField(max_length=100, blank=True)
    downtime_reason = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.service_history_type
